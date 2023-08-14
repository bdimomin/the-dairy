from django import forms
from . models import Transaction, BillInvoices, Quotations

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