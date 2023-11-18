from django.urls import path
from registration import views
from django.urls import path
from . import views

urlpatterns = [
    path('cust_homepage',views.cust_home_page,name='cust_homepage'),
    path('cust_signup/',views.cust_SignupPage,name='cust_signup'),
    path('cust_login/', views.cust_login_view, name='cust_login'),
    path('cust_logout/',views.cust_LogoutPage,name='cust_logout'), 


 
]

    
    
