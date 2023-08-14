from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, email, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('Users must have a phone number')
        
        user= self.model(
            email= self.normalize_email(email),
            name=name,
            phone=phone,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,name, email, phone, password=None):
        user = self.create_user(
            email= self.normalize_email(email),
            name=name,
            phone=phone,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    name= models.CharField(max_length=255)
    email= models.EmailField(max_length=100,unique=True)
    phone= models.CharField(max_length=15,unique=True)
    designation= models.CharField(max_length=100, null=True, blank=True)
    qualification= models.CharField(max_length=100, null=True, blank=True)
    membership_number= models.IntegerField(null=True, blank=True)
    bar_assosciation = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth= models.DateField(null=True, blank=True)
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    gender = models.CharField(max_length=8,choices=GENDER_CHOICES, blank=True, null=True)
    chamber_address = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to="images/", default='images/avatar.webp')
    
    
    #required fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date=models.DateTimeField(auto_now_add=True)
    modified_date=models.DateTimeField(auto_now=True)
    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phone']
    
    objects=UserManager()
    
    def __str__(self):
        return self.name
    
    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True
    
