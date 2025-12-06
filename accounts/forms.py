from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',       
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',    
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name','phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Add placeholders and CSS classes to form fields
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        # Apply 'form-control' CSS class to all fields
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
# Validate that password and confirm_password match
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
# Check if password and confirm_password match if not, raise ValidationError
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match"
            )