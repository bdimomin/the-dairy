from django.shortcuts import render, redirect, HttpResponse
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
from django.db.models import Q
from datetime import datetime

from cases.forms import *
from users.forms import *



def custom_404(request, exception):
    return render(request, '404.html', status=404)


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
    today = date.today()
    last_day =date.today() + timedelta(days=30) 
    all_clients = User.objects.filter(is_superadmin=0).count()
    # running_cases = Case.objects.filter(user=user, status='Running').count()
    new_clients = User.objects.filter(is_superadmin=0,date_joined=date.today()).count()
    active_clients = User.objects.filter(is_superadmin=0,is_active=1).count()
    inactive_clients = User.objects.filter(is_superadmin=0,status="Inactive").count()
    terminated_clients = User.objects.filter(is_superadmin=0,status="Terminate").count()
    upcoming_renewal = User.objects.filter(is_superadmin=0, renewal_date__range=(today,last_day)).count()
    # abandoned_cases = Case.objects.filter(user=user, status='Abandoned').count()

    context = {
        'all_clients': all_clients,
        'new_clients':new_clients,
        'active_clients': active_clients,
        'inactive_clients':inactive_clients,
        'terminated_clients':terminated_clients,
        'upcoming_renewal':upcoming_renewal,
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
    errormessage={}
    if request.method=="POST":
        login_form= UserLoginForm(request.POST)
        if login_form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(request,email=email,password=password)
            
            if user is not None:
                if user.status=="Active":
                   login(request,user)
                   if request.user.is_superadmin==1:
                       return redirect('superadminhome')
                   elif request.user.status=="Active":
                       return redirect('dashboard')
                else:
                    errormessage['message'] = user.status
                
            else:
                return redirect('login_user')
    else:
        login_form= UserLoginForm()
    return render(request,'registration/login.html',{'login_form':login_form,'errormessage':errormessage})

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
    update = StatusUpdateForm()
    no_of_clients=[]
    renewal_dates =[]
    for client in clients:
        abc = Client.objects.filter(user=client.id).count()
        no_of_clients.append(abc)
        dates = Renewal.objects.filter(name_id=client)
        renewal_dates.append(dates)
    xyz = itertools.zip_longest(clients, no_of_clients, renewal_dates)
    
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        status  = request.POST.get('status')
        user = User.objects.get(id=client_id)
        user.status=status
        user.save()
        return redirect('all_clients')
    return render(request, 'superadmin/all_clients.html',{'xyz':xyz,'update':update})


@user_passes_test(superadmin, login_url="/login/")
def registry(request):
    context={}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superadminregistration')
            
        context['registration_form']= form
    else:
        registration = Registration.objects.all()
        form = RegistrationForm()
        context['registration_form']= form
        context['registration']=registration 
    return render(request, 'superadmin/registration.html', context)




@user_passes_test(superadmin, login_url="/login/")
def renewal(request):
    
    if request.method == 'POST':
        name= request.POST.get('name')
        amount = request.POST.get('amount')
        
        one = request.POST.get('days')
        next_renew = date.today() + timedelta(days=int(one))
        users = User.objects.get(id=name)
        
        users.renewal_date= next_renew
        users.save()
        
        
        Renewal.objects.create(name=users, amount=amount, days=next_renew).save()
        return redirect('renewal')
    else:
        today = date.today()
        last_day =date.today() + timedelta(days=30) 
        form = RenewalForm(user=request.user)
        renewal = Renewal.objects.all()
        
        upcoming_renewal = User.objects.filter(is_superadmin=0, renewal_date__range=(today,last_day))
                                               
    return render(request, 'superadmin/renewal.html', {'form':form,'renewal':renewal,'upcoming_renewal':upcoming_renewal})





    
@user_passes_test(superadmin, login_url="/login/")
def expenses(request):
    context={}
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
        context['expenses_form']= form
    else:
        form = ExpensesForm()
        context['expenses_form']= form
        expenses = Expenses.objects.all()
        context['expenses']= expenses
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
    try:
        income = SuperAdminIncomeStatement.objects.all()
        sumincome = SuperAdminIncomeStatement.objects.all().aggregate(sumincome=Sum('amount'))
        expense = SuperAdminExpenseStatement.objects.all()
        sumexpense = SuperAdminExpenseStatement.objects.all().aggregate(sumexpense=Sum('amount'))
        netbalance= sumincome["sumincome"]-sumexpense["sumexpense"]
        balance = itertools.zip_longest(income, expense)
        return render(request,'superadmin/balancestatements.html', {'balance':balance,'netbalance':netbalance})
    except:
        return HttpResponse(" Sorry! No Data Found")
    
@user_passes_test(superadmin, login_url="/login/")
def smsbundle(request):  
    sms = SMSBundle.objects.all()
    form = SMSBundleForm(user=request.user)
    if request.method =='POST':
        client= request.POST.get('client')
        sms_quantity = request.POST.get('sms_quantity')
    
        clients = User.objects.get(id=client)
        
        SMSBundle.objects.create(client=clients, sms_quantity=sms_quantity).save()
        
    return render(request,'superadmin/smsbundle.html', {'form':form,'sms':sms})



@user_passes_test(superadmin, login_url="/login/")
def homepage(request):
    if request.method =='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Homepage.objects.create(title=title, content=content).save()
        return redirect("homepage")
    else:
        homepage = Homepage.objects.all().order_by('-id')
    return render(request, 'superadmin/homepage.html',{'homepage':homepage})


@user_passes_test(superadmin, login_url="/login/")
def homepageupdate(request,pk):
    if request.method =='POST':
        homepage = Homepage.objects.get(id=pk)
        title = request.POST.get('title')
        content = request.POST.get('content')
        homepage.title = title
        homepage.content = content
        homepage.save()
        return redirect("homepage")
    else:
        homepage = Homepage.objects.get(id=pk)
    return render(request, 'superadmin/homepageupdate.html',{'homepage':homepage})

@user_passes_test(superadmin, login_url="/login/")
def homedelete(request,pk):
    homepage = Homepage.objects.get(id=pk)
    homepage.delete()
    return redirect("homepage")


@user_passes_test(superadmin, login_url="/login/")
def aboutpage(request):
    if request.method =='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Aboutpage.objects.create(title=title, content=content).save()
        return redirect("aboutpage")
    else:
        about = Aboutpage.objects.all().order_by('-id')
    return render(request, 'superadmin/about.html',{'about':about})


@user_passes_test(superadmin, login_url="/login/")
def aboutpageupdate(request,pk):
    if request.method =='POST':
        aboutpage = Aboutpage.objects.get(id=pk)
        title = request.POST.get('title')
        content = request.POST.get('content')
        aboutpage.title = title
        aboutpage.content = content
        aboutpage.save()
        return redirect("aboutpage")
    else:
        aboutpage = Aboutpage.objects.get(id=pk)
    return render(request, 'superadmin/aboutpageupdate.html',{'aboutpage':aboutpage})

@user_passes_test(superadmin, login_url="/login/")
def aboutdelete(request,pk):
    aboutpage = Aboutpage.objects.get(id=pk)
    aboutpage.delete()
    return redirect("aboutpage")



@user_passes_test(superadmin, login_url="/login/")
def pricingpage(request):
    if request.method =='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Pricingpage.objects.create(title=title, content=content).save()
        return redirect('pricingpage')
    else:
        pricing = Pricingpage.objects.all().order_by('-id')
    return render(request, 'superadmin/pricing.html',{'pricing':pricing})

@user_passes_test(superadmin, login_url="/login/")
def pricingupdate(request,pk):
    if request.method =='POST':
        pricing = Pricingpage.objects.get(id=pk)
        title = request.POST.get('title')
        content = request.POST.get('content')
        pricing.title = title
        pricing.content = content
        pricing.save()
        return redirect("pricingpage")
    else:
        pricing = Pricingpage.objects.get(id=pk)
    return render(request, 'superadmin/pricingupdate.html',{'pricing':pricing})

@user_passes_test(superadmin, login_url="/login/")
def pricingdelete(request,pk):
    pricing = Pricingpage.objects.get(id=pk)
    pricing.delete()
    return redirect("pricingpage")




