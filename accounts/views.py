import os
from django.shortcuts import render, redirect,get_list_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import date
from num2words import num2words
from . models import Transaction, BillInvoices, Quotations
from . forms import TransactionForm, BillInvoicesForm, QuotationsForm


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
    statements = Transaction.objects.all()
    
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('statements')
    else:
        form = TransactionForm()
    return render(request,'accounts/statements.html',{'statements':statements,'form':form})






def bill_invoices(request):
    bill_invoices = BillInvoices.objects.all()
    form = BillInvoicesForm()
    if request.method == 'POST':
        form=BillInvoicesForm(request.POST)
        if form.is_valid():
            form.save()
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
    due_bills = BillInvoices.objects.filter(is_paid=0)
    return render(request,'accounts/due.html',{'due_bills':due_bills})


def paid_due_bills(request,pk):
    due_bills = BillInvoices.objects.filter(is_paid=0)
    bills = BillInvoices.objects.get(pk=pk)
    bills.is_paid = True
    bills.save()
    return render(request,'accounts/due.html',{'due_bills':due_bills})

def quotations(request):
    quotations = Quotations.objects.all()
    form = QuotationsForm()
    if request.method == 'POST':
        form=QuotationsForm(request.POST)
        if form.is_valid():
            form.save()
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