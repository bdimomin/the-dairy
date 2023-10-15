from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from users.models import Homepage, Aboutpage, Pricingpage

def superadmin(user):
    try:
        return user.is_superadmin
    except:
        pass
    
# @user_passes_test(superadmin, login_url="/login/")
def homepage(request):
    homepage = Homepage.objects.order_by('-id')[0]
    return render(request, 'frontpage/homepage.html',{'homepage': homepage})

# @user_passes_test(superadmin, login_url="/login/")
def about(request):
    aboutpage = Aboutpage.objects.order_by('-id')[0]
    return render(request, 'frontpage/about.html',{'aboutpage':aboutpage})

def pricing(request):
    pricingpage = Pricingpage.objects.order_by('-id')[0]
    return render(request, 'frontpage/pricing.html',{'pricingpage':pricingpage})
