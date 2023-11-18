from django.db import models
from app.models import CustomUserCust
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.db import models

class CustomerAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    billing_address = models.TextField(max_length=200)
    shipping_address = models.TextField(max_length=200)

    def __str__(self):
        return self.name

 
class Product(models.Model):
    supplier_id = models.ForeignKey('Supplier_Detail',null=True, on_delete=models.SET_NULL)
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    description = models.TextField()
    basic_price = models.FloatField()
    transportation_charges = models.FloatField()
    additional_taxes = models.FloatField()
    total_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="oms/images", default="")

    class Meta:
        db_table = 'product_master'

    def __str__(self):
        return self.product_name
    
class Cart(models.Model):
 user = models.ForeignKey(CustomUserCust, on_delete=models.CASCADE)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 quantity = models.PositiveIntegerField(default=1)

 def __str__(self):
  return str(self.id)
  
  # Below Property will be used by checkout.html page to show total cost in order summary
 @property
 def total_cost(self):
   return self.quantity * (self.product.basic_price+self.product.transportation_charges+self.product.additional_taxes)

STATUS_CHOICES = (
  ('Pending','Pending'),
  ('Order_recieved','Order_recieved'),

)

class Order_Placed(models.Model):
    user = models.ForeignKey(CustomUserCust, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerAddress, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    basic_price = models.DecimalField(max_digits=10, decimal_places=2)
    transportation_charges = models.DecimalField(max_digits=10, decimal_places=2)
    additional_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    status = models.CharField(
        max_length=30,
        choices=[
            ('Pending', 'Pending'),
            ('Order Received', 'Order Received'),
        ],
        default='Pending',
    )

    # Add a field to distinguish between "Buy Now" and "Add to Cart"
    order_type = models.CharField(max_length=10,default='buy_now')  # You can use this field to store 'buy_now' or 'add_to_cart'

    ordered_date = models.DateTimeField(auto_now_add=True)

  # Below Property will be used by orders.html page to show total cost
    @property
    def total_cost(self):
        return self.quantity * (self.product.basic_price+self.product.transportation_charges+self.product.additional_taxes)
    

class Order_Received(models.Model):
    product_id = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order_placed = models.ForeignKey(Order_Placed, null=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=80)
    quantity = models.IntegerField()
    basic_price = models.FloatField()
    transportation_charges = models.FloatField()
    additional_taxes = models.FloatField()
    total_amount = models.FloatField()  # Add the total_amount field
    image = models.ImageField(upload_to="oms/images", default="")
    order_received_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=30,
        choices=[
            ('Order Received', 'Order Received'),
            ('Order Confirmed', 'Order Confirmed'),
        ],
        default='Order Received',
    )

    class Meta:
        db_table = 'order_received_master'

    def __str__(self):
        return f'Order_Received({self.product_name}, {self.quantity}, {self.basic_price}, {self.transportation_charges}, {self.additional_taxes}, {self.total_amount}, {self.image})'


class Order_Dispatched(models.Model):
    received_id = models.ForeignKey(Order_Received,null=True, on_delete=models.SET_NULL)
    dispatch_agency = models.CharField(max_length=150)
    order_dispached_date = models.DateTimeField(auto_now_add=True)
    dispatch_manager = models.CharField(max_length=80)
    status = models.CharField(
        max_length=30,
        choices=[
            ('Order Confirmed', 'Order Confirmed'),
            ('Order Dispatched', 'Order Dispatched'),
        ],
        default='Order Confirmed',
    )


    class Meta:
        db_table = 'order_dispatched_master'

    def __str__(self):
        return f'Order_Dispatched({self.Order_Received.product_name}, {self.order_dispatched_date})'

class Order_Transit(models.Model):
    dispatch_id = models.ForeignKey(Order_Dispatched,null=True, on_delete=models.SET_NULL)
    received_id = models.ForeignKey(Order_Received,null=True, on_delete=models.SET_NULL)
    transit_location = models.CharField(max_length=150)
    order_transit_date = models.DateTimeField(auto_now_add=True)
    transit_vehical = models.CharField(max_length=80)
    transit_vehical_driver = models.CharField(max_length=200)
    driver_contact = models.BigIntegerField()
    status = models.CharField(
        max_length=30,
        choices=[
            ('Order Dispatched', 'Order Dispatched'),
            ('Order Transit', 'Order Transit'),
        ],
        default='Order Dispatched',
    )


    class Meta:
        db_table = 'order_transit_master'

    def __str__(self):
        return f'Order_Transit({self.order_id.product_name}, {self.order_transit_date})'



class Supplier_Detail(models.Model):
    supplier_name = models.CharField(max_length=300)
    supplier_contact = models.BigIntegerField()
    supplier_address = models.TextField(max_length=200)
    supplier_gst_no = models.CharField(max_length=20)
    available_quantity = models.IntegerField()
    status = models.CharField(
        max_length=30,
        choices=[
            ('Available', 'Available'),
            ('Not Available', 'Not Available'),
        ],
    )

    class Meta:
        db_table = 'supplier_detail'
    
    def __str__(self):
        return f'''{self.__dict__}'''
    
    def __repr__(self):
        return str(self)
    


from django.db import models

from django.db import models
from django.utils import timezone

class Cancel_Order(models.Model):
    order_id = models.PositiveIntegerField(default=0)  # Add a field to store the order ID
    order_placed = models.ForeignKey('Order_Placed', null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    product_name = models.CharField(max_length=255, default='Unknown')

    quantity = models.PositiveIntegerField(default=0)

    basic_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transportation_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    additional_taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    image = models.ImageField(upload_to='products/', default='default_image.jpg')

    status = models.CharField(max_length=20, default='Cancelled')  # Default status for canceled orders

    cancel_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'cancel_order'

    def __str__(self):
        return f'Canceled Order ({self.product_name}, {self.cancel_date})'
