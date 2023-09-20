from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cases.models import Case,Client
from .models import *
from accounts.models import IncomeStatements
from accounts.forms import IncomeStatementsForm
from datetime import date, timedelta 
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.db.models import Sum
import itertools
from datetime import date

from cases.forms import *
from users.forms import *

def superadmin(user):
    try:
        return user.is_superadmin
    except:
        pass

# Create your views here.
def index(request):
    return render(request,'index.html')


@user_passes_test(superadmin, login_url="/login/")
def home(request):
    all_clients = User.objects.all().count()
    # running_cases = Case.objects.filter(user=user, status='Running').count()
    new_clients = User.objects.filter(date_joined=date.today()).count()
    active_clients = User.objects.filter(is_active=1).count()
    inactive_clients = User.objects.filter(is_active=0).count()
    # decided_cases = Case.objects.filter(user=user, status='Decided').count()
    # abandoned_cases = Case.objects.filter(user=user, status='Abandoned').count()

    context = {
        'all_clients': all_clients,
        'new_clients':new_clients,
        'active_clients': active_clients,
        'inactive_clients':inactive_clients
    }
    return render(request,'superadmin/home.html',context)


@login_required
def dashboard(request):
    user = request.user
    all_cases = Case.objects.filter(user=user).count()
    running_cases = Case.objects.filter(user=user, status='Running').count()
    todays_cases = Case.objects.filter(user=user, date=date.today()).count()
    tomorrows_cases = Case.objects.filter(user=user, date=date.today() + timedelta(days=1)).count()
    not_updated_cases = Case.objects.filter(user=user, updated=False).count()
    decided_cases = Case.objects.filter(user=user, status='Decided').count()
    abandoned_cases = Case.objects.filter(user=user, status='Abandoned').count()

    context = {
        'all_cases': all_cases,
        'running_cases': running_cases,
        'todays_cases': todays_cases,
        'tomorrows_cases': tomorrows_cases,
        'not_updated_cases': not_updated_cases,
        'decided_cases': decided_cases,
        'abandoned_cases': abandoned_cases,
    }
    return render(request, 'dashboard/index.html', context)


def registration(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    context={}
    
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            user= form.save()
            return redirect('login_user')
        context['register_form']=form
    else:
        form= CustomUserForm()
        context['register_form']=form
        
    return render(request,'registration/sign_up.html',context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 

    login_form = UserLoginForm()
    if request.method=="POST":
        login_form= UserLoginForm(request.POST)
        if login_form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
            
            if user is not None:
                login(request,user)
                if request.user.is_superadmin==1:
                    return redirect('superadminhome')
                else:
                    return redirect('dashboard')
            else:
                return redirect('login_user')
    else:
        login_form= UserLoginForm()
    return render(request,'registration/login.html',{'login_form':login_form})

def profile_page(request):
    user = request.user.id
    profile= User.objects.get(id=user)
    return render(request,'dashboard/profile_page.html',{'profile':profile})


def profile_update(request,pk):
    user= User.objects.get(pk=pk)
    form=ProfileUpdateForm(instance=user)
    if request.method == 'POST':
        profile_update=ProfileUpdateForm(request.POST,request.FILES,instance=request.user)
        if profile_update.is_valid():
            profile_update.save()
            return redirect('profile_page')
    return render(request,'dashboard/profile_update.html',{'form':form})

def logout_user(request):
    logout(request)
    return redirect('login_user')


@user_passes_test(superadmin, login_url="/login/")
def new_client(request):
    context={}
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_clients')
        context['register_form']=form
    else:
        form= CustomUserForm()
        context['register_form']=form
    return render(request, 'superadmin/add_client.html', context)

@user_passes_test(superadmin, login_url="/login/")
def all_clients(request):
    clients = User.objects.filter(is_superadmin=0)
    no_of_clients=[]
    for client in clients:
        abc = Client.objects.filter(user=client.id).count()
        no_of_clients.append(abc)
    xyz = zip(clients, no_of_clients)
    return render(request, 'superadmin/all_clients.html',{'xyz':xyz})


@user_passes_test(superadmin, login_url="/login/")
def registry(request):
    context={}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
        context['registration_form']= form
    else:
        form = RegistrationForm()
        context['registration_form']= form
    return render(request, 'superadmin/registration.html', context)

@user_passes_test(superadmin, login_url="/login/")
def renewal(request):
    context={}
    if request.method == 'POST':
        form = RenewalForm(request.POST)
        if form.is_valid():
            form.save()
        context['renewal_form']= form
    else:
        form = RenewalForm()
        context['renewal_form']= form
    return render(request, 'superadmin/renewal.html', context)

@user_passes_test(superadmin, login_url="/login/")
def expenses(request):
    context={}
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
        context['expenses_form']= form
    else:
        form = ExpensesForm()
        context['expenses_form']= form
    return render(request, 'superadmin/expenses.html', context)

@user_passes_test(superadmin, login_url="/login/")
def incomestatemts(request):
    income = SuperAdminIncomeStatement.objects.all()
    form = SuperAdminIncomeStatementForm(user=request.user)
    if request.method =='POST':
        client= request.POST.get('client')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')
        clients = User.objects.get(id=client)
        
        SuperAdminIncomeStatement.objects.create(client=clients, date=date,purpose=purpose,amount=amount).save()
        
    return render(request,'superadmin/incomestatements.html', {'form':form,'income':income})

@user_passes_test(superadmin, login_url="/login/")
def expensestements(request):
    expense = SuperAdminExpenseStatement.objects.all()
    form = SuperAdminExpenseStatementForm(user=request.user)
    if request.method =='POST':
        client= request.POST.get('client')
        date = request.POST.get('date')
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount')
        clients = User.objects.get(id=client)
        
        SuperAdminExpenseStatement.objects.create(client=clients, date=date,purpose=purpose,amount=amount).save()
        
    return render(request,'superadmin/expensestatements.html', {'form':form,'expense':expense})


@user_passes_test(superadmin, login_url="/login/")
def balancestatements(request):  
    income = SuperAdminIncomeStatement.objects.all()
    sumincome = SuperAdminIncomeStatement.objects.all().aggregate(sumincome=Sum('amount'))
    expense = SuperAdminExpenseStatement.objects.all()
    sumexpense = SuperAdminExpenseStatement.objects.all().aggregate(sumexpense=Sum('amount'))
    netbalance= sumincome["sumincome"]-sumexpense["sumexpense"]
    balance = itertools.zip_longest(income, expense)
    return render(request,'superadmin/balancestatements.html', {'balance':balance,'netbalance':netbalance})


