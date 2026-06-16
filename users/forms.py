from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text='Введите ваш номер телефона')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username', 'city')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять только из цифр.')
        return phone_number
