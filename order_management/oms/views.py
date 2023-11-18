from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order_Received, Order_Dispatched, Order_Transit, Supplier_Detail, Cancel_Order,Cart,Order_Placed,CustomerAddress
from app.views import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.db.models import F


def admin_zone(request):
    return render(request, 'admin_zone.html')

def add_product(request):
    if request.method == 'POST':
        supplier_id = request.POST.get("supplier_detail_id")
        try:
            supplier_detail = Supplier_Detail.objects.get(id=supplier_id)
        except Supplier_Detail.DoesNotExist:
            return render(request, 'error_page.html', {"error_message": "Supplier not found"})

        product_name = request.POST['product_name']
        quantity = request.POST['quantity']
        description = request.POST['description']
        basic_price = float(request.POST['basic_price'])
        transportation_charges = float(request.POST['transportation_charges'])
        additional_taxes = float(request.POST['additional_taxes'])

        total_amount = basic_price + transportation_charges + additional_taxes
        image = request.FILES['image']
        
        new_product = Product(
            supplier_id=supplier_detail,
            product_name=product_name,
            description=description,
            basic_price=basic_price,
            transportation_charges=transportation_charges,
            additional_taxes=additional_taxes,
            total_amount=total_amount,
            image=image,
            quantity=quantity
        )
        new_product.save()
        return redirect('product_list')
    return render(request, 'add_product.html', context={"supplier_details": Supplier_Detail.objects.all()})

def update_product(request, id):
    message = ''
    product = Product.objects.filter(id=id).first()

    if request.method == "POST":
        formdata = request.POST
        new_image = request.FILES.get('image')

        if product:
            try:
                product.product_name = formdata.get('product_name')
                product.description = formdata.get('description')
                product.basic_price = formdata.get('basic_price')
                product.transportation_charges = formdata.get('transportation_charges')
                product.additional_taxes = formdata.get('additional_taxes')
                product.quantity = formdata.get('quantity')

                if new_image:
                    product.image = new_image  
                supplier_id = formdata.get('supplier_detail_id')

                try:
                    supplier_detail = Supplier_Detail.objects.get(id=supplier_id)
                    product.supplier_id = supplier_detail
                except Supplier_Detail.DoesNotExist:
                    message = "Supplier not found."

                product.total_amount = (
                    float(formdata.get('basic_price'))
                    + float(formdata.get('transportation_charges'))
                    + float(formdata.get('additional_taxes'))
                )

                product.save()
                message = 'Product Record Updated Successfully...!'
                return redirect('product_list')
            except Exception as e:
                message = "Error Updating Product Record..."
        else:
            message = 'Product not Found...'
    return render(request, 'add_product.html', context={"result": message, 'product': product, 'supplier_details': Supplier_Detail.objects.all()})

def confirm_delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'confirm_delete_product.html', {'product': product})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    return render(request, 'confirm_delete_product.html', {'product': product})


@login_required()
def add_to_cart(request, product_id):
    user = request.user
    product = Product.objects.get(id=product_id)

    if user.is_authenticated:
        selected_quantity = 1 
        is_buy_now = False 

        if request.method == 'POST':
            selected_quantity = int(request.POST.get("selected_quantity", 1))
            is_buy_now = request.POST.get("buy_now") == "true"

        existing_cart_item = Cart.objects.filter(user=user, product=product).first()

        if existing_cart_item:
            existing_cart_item.quantity += selected_quantity
            existing_cart_item.save()
            messages.info(request, 'Product is Already in the cart.')
        else:
            Cart(user=user, product=product, quantity=selected_quantity).save()
            messages.success(request, 'Product added to the cart.')

        if is_buy_now:
            request.session['pending_checkout'] = product.id
            return redirect('checkout')
        else:
            
            return redirect('order')
    return redirect('order')


def view_cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_cost = sum(cart_item.total_cost for cart_item in cart_items)
        
        if not cart_items:
            unit_price = 0 
        else:
            unit_price = cart_items[0].product.basic_price + cart_items[0].product.transportation_charges + cart_items[0].product.additional_taxes

        context = {
            'cart_items': cart_items,
            'total_cost': total_cost,
            'unit_price': unit_price,
        }

        if not cart_items:
            return render(request, 'empty_cart.html')

        return render(request, 'cart.html', context)
    
    # Define context for the case where the user is not authenticated
    context = {}

    return render(request, 'empty_cart.html', context)


 
@require_POST
def update_quantity(request, cart_item_id):
    try:
        cart_item = Cart.objects.get(id=cart_item_id)
        new_quantity = int(request.POST.get('quantity'))
        if new_quantity >= 1:
            cart_item.quantity = new_quantity
            cart_item.save()
            total_cost = cart_item.product.total_amount * cart_item.quantity
        else:
            return HttpResponse('Invalid quantity')
    except Cart.DoesNotExist:
        return HttpResponse('Cart item not found')
    cart_items = Cart.objects.all() 
    total_cost = sum(cart_item.product.total_amount * cart_item.quantity for cart_item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
    })


def remove_from_cart(request, cart_item_id):
    cart_item = Cart.objects.get(id=cart_item_id)

    if cart_item.user == request.user:
        cart_item.delete()
    return redirect('view_cart')


@login_required
def manage_addresses(request):
    user = request.user
    addresses = CustomerAddress.objects.filter(user=user)

    if request.method == 'POST':
        if 'selected_address' in request.POST:
            selected_address_id = request.POST['selected_address']
            selected_address = CustomerAddress.objects.get(id=selected_address_id)
        else:
            new_address = CustomerAddress(
                user=user,
                name=request.POST.get('name'),
                billing_address=request.POST.get('billing_address'),
                shipping_address=request.POST.get('shipping_address'),
            )
            new_address.save()

    context = {
        'addresses': addresses,
    }

    return render(request, 'manage_addresses.html', context)


@login_required
def checkout(request):
    user = request.user
    pending_checkout_item = request.session.get('pending_checkout')
    addresses = CustomerAddress.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    if request.method == 'POST':
        for cart_item in cart_items:
            input_name = 'quantity_' + str(cart_item.id)
            new_quantity = int(request.POST.get(input_name, 1))
            cart_item.quantity = new_quantity
            cart_item.save()

        if pending_checkout_item:
            Cart.objects.filter(user=user, product=pending_checkout_item).delete()
            del request.session['pending_checkout']

        return redirect('order_confirmation') 

    context = {
        'addresses': addresses,
        'cart_items': cart_items,
    }
    return render(request, 'checkout.html', context)


def place_order(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selected_address')
        selected_address = CustomerAddress.objects.get(id=selected_address_id)
        cart_items = Cart.objects.filter(user=request.user)
        orders = []

        for cart_item in cart_items:
            quantity = int(request.POST.get(f'quantity_{cart_item.id}', 1))
            product_name = cart_item.product.product_name
            basic_price = cart_item.product.basic_price
            transportation_charges = cart_item.product.transportation_charges
            additional_taxes = cart_item.product.additional_taxes

            order = Order_Placed.objects.create(
                user=request.user,
                customer=selected_address,
                product=cart_item.product,
                product_name=product_name,
                quantity=cart_item.quantity,
                basic_price=basic_price,
                transportation_charges=transportation_charges,
                additional_taxes=additional_taxes,
                total_amount=cart_item.total_cost,
                image=cart_item.product.image,
                status='Pending',
                order_type='add_to_cart'
            )
            orders.append(order)
            cart_item.product.quantity = F('quantity') - cart_item.quantity
            cart_item.product.save()

        cart_items.delete()

        return render(request, 'order_confirmation.html', {'orders': orders})


def order_confirmation(request):
    latest_order = Order_Placed.objects.filter(user=request.user).latest('ordered_date')

    return render(request, 'order_confirmation.html', {'order': latest_order})


@login_required
def placed_order_list(request):
    if request.user.is_authenticated:
        orders = Order_Placed.objects.filter(user=request.user).order_by('-ordered_date')  

        context = {
            'orders': orders
        }
        return render(request, 'placed_order_list.html', context)
    else:
        return redirect('login') 

 
def pending_orders(request):
    pending_orders = Order_Placed.objects.filter(user=request.user)
    
    context = {
        'orders': pending_orders,
    }
    
    return render(request, 'pending_orders.html', context)


def transfer_order_to_order_received(request, order_id):
    try:
        order_placed = Order_Placed.objects.get(id=order_id)

        order_received = Order_Received(
            product_id=order_placed.product, 
            product_name=order_placed.product_name,
            quantity=order_placed.quantity,
            basic_price=order_placed.basic_price,
            transportation_charges=order_placed.transportation_charges,
            additional_taxes=order_placed.additional_taxes,
            total_amount=order_placed.total_amount,
            image=order_placed.image,
            status='Order Received'
        )

        order_received.save()
        messages.success(request, 'Order Transferred successfully.')
    except Order_Received.DoesNotExist:
        messages.error(request, 'Order not found.')
    return redirect('pending_orders')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})


def product_list_supplier(request, supplier_id):
    supplier = Supplier_Detail.objects.get(id=supplier_id)
    products = Product.objects.filter(supplier_id=supplier)

    return render(request, 'product_list.html', {'products': products, 'supplier': supplier})


def order(request):
    products = Product.objects.all()
    return render(request, 'order.html', {'products': products})


def update_add_product_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'increase':
            product.quantity += 1
        elif action == 'decrease':
            product.quantity = max(0, product.quantity - 1)
        elif action == 'set':
            new_quantity = int(request.POST.get('quantity', 0))
            if new_quantity >= 0:
                product.quantity = new_quantity

        product.total_amount = (product.basic_price + product.transportation_charges + product.additional_taxes) * product.quantity

        product.save()
        products = Product.objects.all()
        return render(request, 'order.html', {'products': products})
    else:
        return render(request, 'order.html', {'error': 'Bad request'}, status=400)


def order_received_list(request):
    orders = Order_Received.objects.all()
    return render(request, 'order_received_list.html', {'orders': orders})


def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST['status']
        order_type = request.POST['order_type']

        if order_type == 'pending':
            try:
                order = Order_Placed.objects.get(id=order_id)
                order.status = new_status
                order.save()

                return redirect('pending_orders')
            except Order_Placed.DoesNotExist:
                messages.error(request, 'Order not found.')

        elif order_type == 'received':
            try:
                order_received = Order_Received.objects.get(id=order_id)
                order_received.status = new_status
                order_received.save()

                try:
                    pending_order = Order_Placed.objects.get(id=order_id)
                    pending_order.status = new_status
                    pending_order.save()
                except Order_Placed.DoesNotExist:
                    messages.error(request, 'Pending Order not found.')

                return redirect('order_received_list')
            except Order_Received.DoesNotExist:
                messages.error(request, 'Order Received not found.')

        elif order_type == 'dispatched':
            try:
                order_dispatched = Order_Dispatched.objects.get(id=order_id)
                order_dispatched.dispatch_agency = request.POST.get('dispatch_agency')
                order_dispatched.dispatch_manager = request.POST.get('dispatch_manager')
                order_dispatched.status = new_status
                order_dispatched.save()

                try:
                    received_order = Order_Received.objects.get(id=order_id)
                    received_order.status = new_status
                    received_order.save()
                except Order_Received.DoesNotExist:
                    messages.error(request, 'Received Order not found.')

                try:
                    pending_order = Order_Placed.objects.get(id=order_id)
                    pending_order.status = new_status
                    pending_order.save()
                except Order_Placed.DoesNotExist:
                    messages.error(request, 'Pending Order not found.')

                return redirect('order_dispatched_list')
            except Order_Dispatched.DoesNotExist:
                messages.error(request, 'Order Dispatched not found.')

        elif order_type == 'transit':
            try:
                order_transit = Order_Transit.objects.get(id=order_id)
                order_transit.transit_location = request.POST.get('transit_location')
                order_transit.transit_vehical = request.POST.get('transit_vehical')
                order_transit.transit_vehical_driver = request.POST.get('transit_vehical_driver')
                order_transit.driver_contact = request.POST.get('driver_contact')
                order_transit.status = new_status
                order_transit.save()

                try:
                    received_order = Order_Received.objects.get(id=order_id)
                    received_order.status = new_status
                    received_order.save()
                except Order_Received.DoesNotExist:
                    messages.error(request, 'Received Order not found.')

                try:
                    dispatched_order = Order_Dispatched.objects.get(id=order_id)
                    dispatched_order.status = new_status
                    dispatched_order.save()
                except Order_Dispatched.DoesNotExist:
                    messages.error(request, 'Dispatched Order not found.')

                try:
                    pending_order = Order_Placed.objects.get(id=order_id)
                    pending_order.status = new_status
                    pending_order.save()
                except Order_Placed.DoesNotExist:
                    messages.error(request, 'Pending Order not found.')

                return redirect('order_transit_list')
            except Order_Transit.DoesNotExist:
                messages.error(request, 'Order Transit not found.')


    return redirect('some_error_page')


def transfer_order_to_dispatched(request, order_id):
    try:
        order_received = Order_Received.objects.get(id=order_id)

        order_dispatched = Order_Dispatched(
            received_id=order_received,
            dispatch_agency='Your Dispatch Agency Value', 
            order_dispached_date="2023-10-17",  
            dispatch_manager='Your Dispatch Manager Value',  
            status='Order Confirmed' 
        )
        order_dispatched.save()
        messages.success(request, 'Order Transferred successfully.')
    except Order_Received.DoesNotExist:
        messages.error(request, 'Order not found.')
    return redirect('order_received_list')


def order_dispatched_list(request):
    orders_dispatched = Order_Dispatched.objects.all()
    return render(request, 'order_dispatched_list.html', {'orders_dispatcheds': orders_dispatched})



def transfer_order_to_transit(request, order_id):
    try:
        order_dispatched = Order_Dispatched.objects.get(id=order_id)
        order_received = order_dispatched.received_id  

        order_transit = Order_Transit(
            dispatch_id=order_dispatched,
            received_id=order_received, 
            transit_location='Your Transit Location',
            order_transit_date='2023-10-17',
            transit_vehical='Your Transit Vehicle',
            transit_vehical_driver='Your Transit Vehicle Driver',
            driver_contact='1234567890',
            status='Order Dispatched'
        )
        order_transit.save()
        
        messages.success(request, 'Order Transferred to Transit successfully.')
    except Order_Dispatched.DoesNotExist:
        messages.error(request, 'Order Dispatched not found.')
    return redirect('order_dispatched_list')


def order_transit_list(request):
    order_transit = Order_Transit.objects.all()
    return render(request, 'order_transit_list.html', {'orders_transits': order_transit})



def Supplier_Detail_Create(request):
    message = ''
    if request.method == "POST":
        formdata = request.POST
        try:
            supplier_detail = Supplier_Detail.objects.create(
                supplier_name=formdata.get('supplier_name'),
                supplier_contact=formdata.get('supplier_contact'),
                supplier_address=formdata.get('supplier_address'),
                supplier_gst_no=formdata.get('supplier_gst_no'),
                available_quantity=formdata.get('available_quantity'),
                status=formdata.get('status'),
            )
            message = "Supplier detail record saved successfully...!"
        except Exception as e:
            message = f"Error saving supplier detail record: {str(e)}"
    return render(request, template_name="Supplier_Detail_Create.html", context={"result": message})


def supplier_detail_list(request):
    search_query = request.GET.get('search_query', '')

    if search_query:
        supplier_details = Supplier_Detail.objects.filter(supplier_name__icontains=search_query)
    else:
        supplier_details = Supplier_Detail.objects.all()

    return render(request, 'supplier_detail_list.html', {'supplier_details': supplier_details, 'search_query': search_query})



def cancel_order(request, order_placed_id):
    try:
        order_placed = Order_Placed.objects.get(pk=order_placed_id)

        if request.method == 'POST':

            cancel_order = Cancel_Order(
                order_id=order_placed.id,
                order_placed=order_placed,
                product=order_placed.product,
                product_name=order_placed.product_name,
                quantity=order_placed.quantity,
                basic_price=order_placed.basic_price,
                transportation_charges=order_placed.transportation_charges,
                additional_taxes=order_placed.additional_taxes,
                total_amount=order_placed.total_amount,
                image=order_placed.image,
                status='Cancelled'  
            )
            cancel_order.save()

            order_placed.status = 'Cancelled'
            order_placed.save()

            return redirect('placed_order_list')

        return render(request, 'placed_order_list.html', {'order_placed': order_placed})

    except Order_Placed.DoesNotExist:
        return render(request, 'order_not_found.html')
    
def cancel_order_list(request):
    canceled_orders = Cancel_Order.objects.all()

    return render(request, 'cancel_order_list.html', {'canceled_orders': canceled_orders})