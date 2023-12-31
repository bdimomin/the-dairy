from django.db import models
from cases.models import Client, Case
from users.models import User

# Create your models here.

class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('Income','Income'),
        ('Expense','Expense'),
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
    party_name = models.CharField(max_length=50)
    details = models.TextField(blank=True,null=True)
    amount = models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f"Date: {self.date}, Client: {self.party_name}"
    
    
class BillInvoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length=150,null=True,blank=True)
    subjects= models.CharField(max_length=255, blank=True, null=True)
    date= models.DateField(auto_now_add=True)
    description= models.TextField(blank=True, null=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    vat=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    # Total_amount=models.DecimalField(max_digits=6,decimal_places=2, blank=True, null=True)
    is_paid= models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.subjects
    
class Quotations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.CharField(max_length=150,null=True,blank=True)
    subjects= models.CharField(max_length=255, blank=True, null=True)
    date= models.DateField(auto_now_add=True)
    description= models.TextField(blank=True, null=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    vat=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    is_paid= models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.subjects
    
    
class IncomeStatements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    purpose = models.CharField(max_length=150,null=True,blank=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    
    def __str__(self):
        return self.client
    
class ExpenseStatements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    purpose = models.CharField(max_length=150,null=True,blank=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    
    def __str__(self):
        return self.client
    
class DueStatements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    purpose = models.CharField(max_length=150,null=True,blank=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    
    def __str__(self):
        return self.client
    
class VatStatements(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)
    client= models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    purpose = models.CharField(max_length=150,null=True,blank=True)
    amount=models.DecimalField(max_digits=19, decimal_places=2,blank=True, null=True)
    
    def __str__(self):
        return self.client
    

    
    