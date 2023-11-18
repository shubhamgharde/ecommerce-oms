from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    # path('', views.add_product_list, name='home'),
    path('', views.order, name='order'),

    path('admin_zone/', views.admin_zone, name='admin_zone'),

    path('add_product/', views.add_product, name='add_product'),
    path('update_product/<int:id>/', views.update_product, name='update_product'),
    # path('edit/<int:id>/', views.edit_product, name='edit'),
    path('home/', views.order, name='home'),
    path('order/', views.order, name='order'),
    path('product_list/', views.product_list, name='product_list'),
    path('product_list_supplier/<int:supplier_id>/', views.product_list_supplier, name='product_list_supplier'),

    path('order_received/', views.Order_Received, name='order_received'),

   
    path('update_add_product_quantity/<int:product_id>/', views.update_add_product_quantity, name='update_add_product_quantity'),

    path('confirm_delete_product/<int:id>/', views.confirm_delete_product, name='confirm_delete_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),


    path('order_received_list/', views.order_received_list, name='order_received_list'),
    # path('update_order_received_status/<int:order_id>/', views.update_order_received_status, name='update_order_received_status'),
    path('transfer_order_to_dispatched/<int:order_id>/', views.transfer_order_to_dispatched, name='transfer_order_to_dispatched'),
    
    path('transfer_order_to_transit/<int:order_id>/', views.transfer_order_to_transit, name='transfer_order_to_transit'),
    path('order_dispatched_list/', views.order_dispatched_list, name='order_dispatched_list'),
    # path('update_order_dispatched_status/<int:order_id>/', views.update_order_dispatched_status, name='update_order_dispatched_status'),

    # path('order_transit/<int:order_id>/', views.order_transit, name='order_transit'),
    path('order_transit_list/', views.order_transit_list, name='order_transit_list'),
    # path('update_order_transit_status/<int:order_id>/', views.update_order_transit_status, name='update_order_transit_status'),
    

    path('supplier_detail/create/', views.Supplier_Detail_Create, name='Supplier_Detail_Create'), 
    path('supplier_detail_list/', views.supplier_detail_list, name='supplier_detail_list'),
    
    path('cancel_order/<int:order_placed_id>/', views.cancel_order, name='cancel_order'),



    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    # path('cust_login/', LoginView.as_view(), name='cust_login'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('manage-addresses/', views.manage_addresses, name='manage_addresses'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),  # Define the URL pattern for order_confirmation
    path('update_quantity/<int:cart_item_id>/', views.update_quantity, name='update_quantity'),


    path('placed_order_list/', views.placed_order_list, name='placed_order_list'),
   
    
    path('pending-orders/', views.pending_orders, name='pending_orders'),
    
    # path('update_pending_order_status/<int:order_id>/', views.update_pending_order_status, name='update_pending_order_status'),
    path('transfer_order_to_order_received/<int:order_id>/', views.transfer_order_to_order_received, name='transfer_order_to_order_received'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    # path('update_order_status/<int:order_id>/', views.OrderStatusUpdateView.as_view(), name='update_order_status'),

    path('cancel-order-list/', views.cancel_order_list, name='cancel_order_list'),
]