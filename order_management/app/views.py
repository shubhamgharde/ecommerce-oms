
from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.db import IntegrityError
from django.contrib.auth import logout
from .validators import *
from .models import CustomUserCust
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib import messages



def cust_home_page(request):
    return render(request, template_name='cust_homepage.html')

def cust_SignupPage(request):
    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!!")
        else:
            try:
                # Validate email format
                email_validator = EmailValidator()
                email_validator(email)

                custom_validators = [
                    CustMinimumLengthValidator(min_length=8),
                    CustNumericCharacterValidator(),
                    CustUppercaseCharacterValidator(),
                    CustLowercaseCharacterValidator(),
                    CustSpecialCharacterValidator(),
                ]

                # Validate password
                # validate_password(pass1)
                validate_password(pass1, user=None, password_validators=custom_validators)

                    # Create a user using the CustomUser model
                my_user = CustomUserCust.objects.create_user(
                    email=email,
                    password=pass1,
                    
                )
                
                my_user.first_name = name  # Set the first name to the provided name
                my_user.save()                    
                messages.success(request, "User created successfully!")
                return HttpResponseRedirect('/cust_login/')
            except DjangoValidationError as e:
                if hasattr(e, 'error_dict') and 'email' in e.error_dict:
                    email_error = e.error_dict['email'][0]
                if hasattr(e, 'messages') and 'password' in e.messages:
                    password_error = ', '.join(e.messages['password'])
                messages.error(request, f"{str(e)}")
            except IntegrityError as e:
                messages.error(request, "An account with that email already exists.")
            except Exception as e:
                messages.error(request, f"{str(e)}")

    return render(request, 'cust_signup.html')


 
def cust_LogoutPage(request):
    logout(request)
    return redirect('cust_login')


def cust_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('order')
        else:
            return render(request, 'cust_login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'cust_login.html')










