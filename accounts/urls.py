from django.urls import path

from . import views

urlpatterns = [
    # path('entry-transaction/',views.entry_transaction, name='all_transactions'),
    path('statements/',views.get_statements, name='statements'),
    path('bill-invoices/',views.bill_invoices, name="bill_invoices"),
    path('bill-invoice/<int:pk>/',views.onebill_invoice,name="oneBillInvoice"),
    path('genbillpdf/<int:pk>/',views.billinvoicePDF,name="BillInvoicePDF"),
    path('due_bills/',views.due_bills, name="due_bills"),
    path('due_bills/<int:pk>',views.paid_due_bills, name="paid_due_bills"),
    path('quotations/',views.quotations,name="quotations"),
    path('quotation/<int:pk>/',views.oneQuotation,name="oneQuotation"),
    path('genquopdf/<int:pk>/',views.quotationPdf,name="QuotationPDF"),
]