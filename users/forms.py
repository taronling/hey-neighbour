# Form Imports
from django import forms
from django.forms import Textarea, EmailInput

# Internal Imports
from .models import User

class SignUpForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')

        labels = {
            'email': ('Email'),
        }
        help_texts = {
            'email': ('Some useful help text.'),
        }
        error_messages = {
            'email': {
                'max_length': ("This writer's name is too long."),
            },
        }
        widgets = {
            # 'first_name': Textarea(attrs={'cols': 80, 'rows': 1}),
            'email': EmailInput(attrs={'class': 'form-control'}),
        }