from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('registration/',views.registration, name="registration"),
    path('home/',views.dashboard,name='dashboard'),
    path('login/',views.login_view,name='login_user'),
    path('logout/',views.logout_user,name='logout_user'),
    path('profile/update/<int:pk>/',views.profile_update, name='profile_update'),
    path('profile/',views.profile_page, name='profile_page'),
    
    path('useradmin-home/', views.home, name="superadminhome"),
    path('useradmin/new-client/', views.new_client, name="new_client"),
    path('useradmin/all-clients/', views.all_clients, name="all_clients"),
    path('useradmin/registration/', views.registry, name="superadminregistration"),
    path('useradmin/renewal/', views.renewal, name="renewal"),
    path('useradmin/expenses/', views.expenses, name="expenses"),
    
    path('useradmin/income-statement/', views.incomestatemts, name="superadminIncomeStatement"),
    path('useradmin/expense-statement/', views.expensestements, name="superadminExpenseStements"),
    path('useradmin/balance-statement/', views.balancestatements, name="superadminBalanceStatement"),
    path('useradmin/sms-bundle/', views.smsbundle, name="smsbundle"),
    
    
    path('useradmin/homepage/', views.homepage, name="homepage"),
    path('useradmin/homepage/<int:pk>/', views.homepageupdate, name="homepageupdate"),
    path('useradmin/home-delete/<int:pk>/', views.homedelete, name="homedelete"),
    
    path('useradmin/about/', views.aboutpage, name="aboutpage"),
    path('useradmin/about/<int:pk>/', views.aboutpageupdate, name="aboutpageupdate"),
    path('useradmin/about-delete/<int:pk>/', views.aboutdelete, name="aboutdelete"),
    
    path('useradmin/pricing/', views.pricingpage, name="pricingpage"),
    path('useradmin/pricing/<int:pk>/', views.pricingupdate, name="pricingupdate"),
    path('useradmin/pricing-delete/<int:pk>/', views.pricingdelete, name="pricingdelete"),
    
]
