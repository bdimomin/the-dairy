from django.shortcuts import render, redirect
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm, UserLoginForm, ProfileUpdateForm
from cases.models import Case
from users.models import CustomUser
from datetime import date, timedelta 

# Create your views here.
def index(request):
    return render(request,'index.html')

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
                return redirect('dashboard')
            else:
                return redirect('login_user')
    else:
        login_form= UserLoginForm()
    return render(request,'registration/login.html',{'login_form':login_form})

def profile_page(request):
    user = request.user.id
    profile= CustomUser.objects.get(id=user)
    return render(request,'dashboard/profile_page.html',{'profile':profile})


def profile_update(request,pk):
    user= CustomUser.objects.get(pk=pk)
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