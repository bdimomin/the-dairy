from django import forms
from . models import Transaction, BillInvoices, Quotations, IncomeStatements,ExpenseStatements,DueStatements,VatStatements
from cases.models import Client
from users.models import CustomUser

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class BillInvoicesForm(forms.ModelForm):
    class Meta:
        model = BillInvoices
        exclude = ['is_paid']
    
    def __init__(self, user=None, **kwargs):
        super(BillInvoicesForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset = Client.objects.filter(user=user)
        
class QuotationsForm(forms.ModelForm):
    class Meta:
        model= Quotations
        exclude = ['is_paid']
        
    def __init__(self, user=None, **kwargs):
        super(QuotationsForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset = Client.objects.filter(user=user)
        
        

class IncomeStatementsForm(forms.ModelForm):
    class Meta:
        model = IncomeStatements
        exclude = ['user']
        
    def __init__(self, user=None, **kwargs):
        super(IncomeStatementsForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset = Client.objects.filter(user=user)
        
class ExpenseStatementsForm(forms.ModelForm):
    class Meta:
        model = ExpenseStatements
        exclude = ['user']
        
    def __init__(self, user=None, **kwargs):
        super(ExpenseStatementsForm, self).__init__(**kwargs)
        if user:
            self.fields['client'].queryset = Client.objects.filter(user=user)

class DueStatementsForm(forms.ModelForm):
    class Meta:
        model = DueStatements
        exclude = ['user']
        
class VatStatementsForm(forms.ModelForm):
    class Meta:
        model = VatStatements
        exclude = ['user']
        