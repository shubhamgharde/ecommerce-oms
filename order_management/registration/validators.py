# validators.py
from django.core.exceptions import ValidationError
import datetime

class MinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(f"Password must be at least {self.min_length} characters long.")

class NumericCharacterValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")

class UppercaseCharacterValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")

class LowercaseCharacterValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
class SpecialCharacterValidator:
    def validate(self, password, user=None):
        special_characters = "!@#$%^&*()_+[]{}|;:'\",.<>?`~"
        if not any(char in special_characters for char in password):
            raise ValidationError("Password must contain at least one special character.")
        
