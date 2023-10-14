from django import forms
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class CustomUserForm(UserCreationForm):

    class Meta:
        model=User
        fields=['name','email','phone','password1','password2']

        

class UserLoginForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['email', 'password']
        
    def clean(self):
        if self.is_valid():
            email=self.cleaned_data['email']
            password=self.cleaned_data['password']
            
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Credentials")
            
            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['name','email','phone','designation','qualification','membership_number','bar_assosciation','date_of_birth','gender','chamber_address','photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }  
        
class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields=['name','email','mobile','amount',]
        
        
class RenewalForm(forms.ModelForm):
    class Meta:
        model = Renewal
        fields=['name','amount', 'days']
        
    def __init__(self, user=None, **kwargs):
        super(RenewalForm, self).__init__(**kwargs)
        if user:
            self.fields['name'].queryset =User.objects.filter(is_superadmin=0)
        
class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields=['purpose','amount']
        
class SuperAdminIncomeStatementForm(forms.ModelForm):
    class Meta:
        model = SuperAdminIncomeStatement
        fields = '__all__'
        
    def __init__(self, user=None, **kwargs):
        super(SuperAdminIncomeStatementForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset =User.objects.filter(is_superadmin=0)
class SuperAdminExpenseStatementForm(forms.ModelForm):
    class Meta:
        model = SuperAdminExpenseStatement
        fields = '__all__'
        
    def __init__(self, user=None, **kwargs):
        super(SuperAdminExpenseStatementForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset =User.objects.filter(is_superadmin=0)
class SMSBundleForm(forms.ModelForm):
    class Meta:
        model = SMSBundle
        fields = '__all__'
        
    def __init__(self, user=None, **kwargs):
        super(SMSBundleForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset =User.objects.filter(is_superadmin=0)
        

class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['status']
        
    def __init__(self, *args, **kwargs):
        super(StatusUpdateForm, self).__init__(*args, **kwargs)
        self.fields['status'].label = False
        
        