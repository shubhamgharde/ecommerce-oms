
from django.contrib.auth import login, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import logout
from .validators import *
from .models import CustomUser
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib import messages
from django.contrib.auth import get_user_model





def index(request):
    return render(request, template_name='index.html')

def home_page(request):
    return render(request, template_name='homepage.html')

def SignupPage(request):
    message = ''
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        contact = request.POST.get('contact')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        aadhaar = request.POST.get('aadhaar')
        marital_status = request.POST.get('marital_status')
        spouse_name = request.POST.get('spouse_name')
        department = request.POST.get('department')
        dpt_manager = request.POST.get('dpt_manager')
        qualification = request.POST.get('qualification')
        designation = request.POST.get('designation')
        grade_pay = request.POST.get('grade_pay')
        basic_pay = request.POST.get('basic_pay')
        taxation = request.POST.get('taxation')
        project = request.POST.get('project')
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')

        

        if pass1 != pass2:
            messages.error(request, "Your password and confirm password are not the same!!")
        else:
            try:
                # Validate email format
                email_validator = EmailValidator()
                email_validator(email)

                custom_validators = [
                    MinimumLengthValidator(min_length=8),
                    NumericCharacterValidator(),
                    UppercaseCharacterValidator(),
                    LowercaseCharacterValidator(),
                    SpecialCharacterValidator(),
                ]

                # Validate password
                # validate_password(pass1)
                validate_password(pass1, user=None, password_validators=custom_validators)
                grade_pay = request.POST.get('grade_pay')

                if not (aadhaar.isdigit() and len(aadhaar) == 12):
                    messages.error(request, "Aadhaar number must be a 12-digit number.")

                else:
                    if not grade_pay:
                        grade_pay = None
                    basic_pay = request.POST.get('basic_pay')
                    if not basic_pay:
                        basic_pay = None  # Set it to None if it's empty
                    taxation = request.POST.get('taxation')
                    if not taxation:
                        taxation = None  # Set it to None if it's empty

                    # Create a user using the CustomUser model
                    my_user = CustomUser.objects.create_user(
                        email=email,
                        password=pass1,
                        contact=contact,
                        dob=dob,
                        address=address,
                        aadhaar=aadhaar,
                        marital_status=marital_status,
                        spouse_name=spouse_name,
                        department=department,
                        dpt_manager=dpt_manager,
                        qualification=qualification,
                        designation=designation,
                        grade_pay=grade_pay,
                        basic_pay=basic_pay,
                        taxation=taxation,
                        project=project,
                        security_question=security_question,
                        security_answer=security_answer,
                    )
                    
                    my_user.first_name = name  # Set the first name to the provided name
                    my_user.save()                    
                    messages.success(request, "User created successfully!")
                    return HttpResponseRedirect('/login/')
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

    return render(request, 'signup.html')


 
def LogoutPage(request):
    logout(request)
    return redirect('login')

def get_all_users(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})



def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'admin_zone.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')








CustomUser = get_user_model()

def ForgotPasswordPage(request):
    result = ''

    if request.method == 'POST':
        email = request.POST.get('email')
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        try:
            user = CustomUser.objects.get(email=email)
            if (
                user.security_question == security_question
                and user.security_answer == security_answer
                and new_password == confirm_password
            ):
                custom_validators = [
                    MinimumLengthValidator(min_length=8),
                    NumericCharacterValidator(),
                    UppercaseCharacterValidator(),
                    LowercaseCharacterValidator(),
                    SpecialCharacterValidator(),
                ]
                validate_password(new_password, user=None, password_validators=custom_validators)
                
                user.set_password(new_password)
                user.save()
                return redirect('login')
            else:
                result = "Invalid email, security question, or security answer."
        except CustomUser.DoesNotExist:
            result = "No user with that email exists."
        except ValidationError as e:
            result = ', '.join(e.messages)
        except Exception as e:
            result = f"An error occurred: {str(e)}"

    return render(request, 'forgot_password.html', {"result": result})


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser  # Import your CustomUser model

@login_required
def edit_profile_view(request):

    if request.method == 'POST':
        form_data = request.POST
        user = request.user  # Get the logged-in user
        # user.first_name = form_data.get('name')
        # user.email = form_data.get('email')
        user.contact = form_data.get('contact')
        # user.dob = form_data.get('dob')
        user.address = form_data.get('address')
        # user.aadhaar = form_data.get('aadhaar')
        # user.marital_status = form_data.get('marital_status')
        user.spouse_name = form_data.get('spouse_name')
        # user.department = form_data.get('department')
        # user.dpt_manager = form_data.get('dpt_manager')
        user.qualification = form_data.get('qualification')
        # user.designation = form_data.get('designation')
        # user.grade_pay = form_data.get('grade_pay')
        # user.basic_pay = form_data.get('basic_pay')
        # user.taxation = form_data.get('taxation')
        # user.project = form_data.get('project')
        # user.security_question = form_data.get('security_question')
        # user.security_answer = form_data.get('security_answer')

        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('index')  # Redirect to the user's profile page
    
    else:
        # Pre-fill the form with the user's current information
        user = request.user
        form_data = {
            # 'name': user.first_name,
            # 'email': user.email,
            'contact': user.contact,
            # 'dob': user.dob,
            'address': user.address,
            # 'aadhaar': user.aadhaar,
            # 'marital_status': user.marital_status,
            'spouse_name': user.spouse_name,
            # 'department': user.department,
            # 'dpt_manager': user.dpt_manager,
            'qualification': user.qualification,
            # 'designation': user.designation,
            # 'grade_pay': user.grade_pay,
            # 'basic_pay': user.basic_pay,
            # 'taxation': user.taxation,
            # 'project': user.project,
            # 'security_question': user.security_question,
            # 'security_answer': user.security_answer,
        }

    return render(request, 'edit_profile.html', {'form_data': form_data})
