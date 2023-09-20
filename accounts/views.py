import os

from django.shortcuts import render, redirect,get_list_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from django.db.models import Sum
import itertools
from num2words import num2words
from . models import Transaction, BillInvoices, Quotations,IncomeStatements,ExpenseStatements,DueStatements, VatStatements
from . forms import TransactionForm, BillInvoicesForm, QuotationsForm, IncomeStatementsForm,ExpenseStatementsForm,DueStatementsForm, VatStatementsForm
from cases.models import Client
from users.models import User

# Create your views here.

# def entry_transaction(request):
#     if request.method == 'POST':
#         form = TransactionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('statements')
#     else:
#         form = TransactionForm()
#     return render(request, 'accounts/entry_transaction.html',{'form':form})




def get_statements(request):
    user = request.user.id
    statements = Transaction.objects.filter(user=user)
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('statements')
    else:
        form = TransactionForm()
    return render(request,'accounts/statements.html',{'statements':statements,'form':form})






def bill_invoices(request):
    user = request.user.id
    bill_invoices = BillInvoices.objects.filter(user=user)
    form = BillInvoicesForm(user=request.user)
    if request.method == 'POST':
        user = request.user.id
        client= request.POST.get('client')
        address= request.POST.get('address')
        subjects = request.POST.get('subjects')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        vat = request.POST.get('vat')
        
        user = User.objects.get(id=user)
        client = Client.objects.get(id=client)
        BillInvoices.objects.create(user=user,client=client, address=address, subjects=subjects,description=description, amount=amount, vat=vat).save()
      
    return render(request,'accounts/bill_invoices.html',{'bill_invoices':bill_invoices,'form':form})


def onebill_invoice(request,pk):
    bill_invoice=BillInvoices.objects.get(pk=pk)
    total = bill_invoice.amount + bill_invoice.vat
    word= num2words(total)
    return render(request,'accounts/one_bill_invoice.html',{'bill_invoice':bill_invoice,'word':word})


def billinvoicePDF(request, *args, **kwargs):
    pk = kwargs.get('pk')
    billInvoice=BillInvoices.objects.get(pk=pk)
    user = request.user
    today = date.today()
    total = billInvoice.amount + billInvoice.vat
    word= num2words(total)
    template_path = 'accounts/bill_invoice_pdf.html'
    context = {'billInvoice': billInvoice,'user':user,'today':today,'word':word}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = 'filename="bill_invoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def due_bills(request):
    user = request.user.id
    due_bills = BillInvoices.objects.filter(user=user,is_paid=0)
    return render(request,'accounts/due.html',{'due_bills':due_bills})


def paid_due_bills(request,pk):
    user = request.user.id
    due_bills = BillInvoices.objects.filter(user=user, is_paid=0)
    bills = BillInvoices.objects.get(pk=pk)
    bills.is_paid = True
    bills.save()
    return render(request,'accounts/due.html',{'due_bills':due_bills})





def quotations(request):
    user = request.user.id
    quotations = Quotations.objects.filter(user=user)
    form = QuotationsForm(user=request.user)
    if request.method == 'POST':
        user = request.user.id
        client= request.POST.get('client')
        address= request.POST.get('address')
        subjects = request.POST.get('subjects')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        vat = request.POST.get('vat')
        
        user = User.objects.get(id=user)
        client = Client.objects.get(id=client)
        Quotations.objects.create(user=user,client=client, address=address, subjects=subjects,description=description, amount=amount, vat=vat).save()
        
    return render(request,'accounts/quotations.html',{'quotations':quotations,'form':form})





def oneQuotation(request,pk):
    quotation=Quotations.objects.get(pk=pk)
    total = quotation.amount + quotation.vat
    word= num2words(total)
    return render(request,'accounts/oneQuotation.html',{'quotation':quotation,'word':word})


def quotationPdf(request, *args, **kwargs):
    pk = kwargs.get('pk')
    quotation=Quotations.objects.get(pk=pk)
    user = request.user
    today = date.today()
    total = quotation.amount + quotation.vat
    word= num2words(total)
    template_path = 'accounts/quotationpdf.html'
    context = {'quotation': quotation,'user':user,'today':today,'word':word}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    
    response['Content-Disposition'] = 'filename="quotation.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def incomestatemts(request):  
    user = request.user.id
    income = IncomeStatements.objects.filter(user=user)
    form = IncomeStatementsForm(user=request.user)
    if request.method =='POST':
        user = request.user.id
        client= request.POST.get('client')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')
        user = User.objects.get(id=user)
        client = Client.objects.get(id=client)
        
        IncomeStatements.objects.create(user=user,client=client, date=date,purpose=purpose,amount=amount).save()
        
    return render(request,'accounts/incomestatements.html', {'form':form,'income':income})

def expensestatements(request):  
    user = request.user.id
    expense = ExpenseStatements.objects.filter(user=user)
    form = ExpenseStatementsForm(user=request.user)
    if request.method =='POST':
        user = request.user.id
        client= request.POST.get('client')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')
        user = User.objects.get(id=user)
        client = Client.objects.get(id=client)
        
        ExpenseStatements.objects.create(user=user,client=client, date=date,purpose=purpose,amount=amount).save()
        
    return render(request,'accounts/expensestatements.html', {'form':form,'expense':expense})


def balancestatements(request):  
    
    try:
        user = request.user.id
        income = IncomeStatements.objects.filter(user=user)
        sumincome = IncomeStatements.objects.filter(user=user).aggregate(sumincome=Sum('amount'))
        expense = ExpenseStatements.objects.filter(user=user)
        sumexpense = ExpenseStatements.objects.filter(user=user).aggregate(sumexpense=Sum('amount'))
        netbalance= sumincome["sumincome"]-sumexpense["sumexpense"]
        balance = itertools.zip_longest(income, expense)
        return render(request,'accounts/balancestatements.html', {'balance':balance,'netbalance':netbalance})
    except:
        return HttpResponse("Sorry! No Data Found!")
    
    