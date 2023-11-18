from django.urls import path
from registration import views
from django.urls import path
from . import views

urlpatterns = [
    path('homepage/',views.home_page,name='homepage'),
    path('signup/',views.SignupPage,name='signup'),
    path('home/',views.index,name='index'), 
    path('user-list/', views.get_all_users, name='user_list'),
    path('login/', views.login_view, name='login'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('forgot-password/', views.ForgotPasswordPage, name='forgot_password'),
     path('logout/',views.LogoutPage,name='logout'), 
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),

 
]

    
    
