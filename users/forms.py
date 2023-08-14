from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

class CustomUserForm(UserCreationForm):

    class Meta:
        model=CustomUser
        fields=['name','email','phone','password1','password2']

        

class UserLoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model=CustomUser
        fields=['email', 'password']
        
    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Credentials")
            
            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=CustomUser
        fields=['name','email','phone','designation','qualification','membership_number','bar_assosciation','date_of_birth','gender','chamber_address','photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }  