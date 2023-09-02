from django import forms
from . models import Transaction, BillInvoices, Quotations, IncomeStatements,ExpenseStatements,DueStatements,VatStatements

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'


class BillInvoicesForm(forms.ModelForm):
    class Meta:
        model = BillInvoices
        exclude = ['is_paid']
        
class QuotationsForm(forms.ModelForm):
    class Meta:
        model= Quotations
        exclude = ['is_paid']

class IncomeStatementsForm(forms.ModelForm):
    class Meta:
        model = IncomeStatements
        exclude = ['user']
        
class ExpenseStatementsForm(forms.ModelForm):
    class Meta:
        model = ExpenseStatements
        exclude = ['user']

class DueStatementsForm(forms.ModelForm):
    class Meta:
        model = DueStatements
        exclude = ['user']
        
class VatStatementsForm(forms.ModelForm):
    class Meta:
        model = VatStatements
        exclude = ['user']
        