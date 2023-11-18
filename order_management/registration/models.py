from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    contact = models.BigIntegerField()
    dob = models.DateField()
    address = models.CharField(max_length=255)
    aadhaar = models.CharField(max_length=12, unique=True)
    marital_status = models.CharField(max_length=20)
    spouse_name = models.CharField(max_length=30, blank=True)
    department = models.CharField(max_length=50)
    dpt_manager = models.CharField(max_length=50)
    qualification = models.CharField(max_length=50)
    designation = models.CharField(max_length=50)
    grade_pay = models.FloatField(blank=True, null=True)
    basic_pay = models.FloatField(blank=True, null=True)
    taxation = models.FloatField(blank=True, null=True)
    project = models.CharField(max_length=50)
    security_question = models.CharField(max_length=255, null=True, blank=True)
    security_answer = models.CharField(max_length=255, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'contact', 'dob','address', 'aadhaar', 'marital_status', 'department', 'dpt_manager', 'qualification', 'designation', 'project','security_question','security_answer']  # Add other required fields as needed
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='registration_users'  # Specify a unique related_name
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='registration_users_permissions'  # Specify a unique related_name
    )
