from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from .models import Momo,Category

# Create your views here.

date=datetime.now()

# @login_required(login_url='log_in')
def index(request):
    cate=Category.objects.all()
    
    cateid=request.GET.get('category')
    if cateid:
        data=Momo.objects.filter(category=cateid)
    else:
        data=Momo.objects.all()
    context={
        'date':date,
        'cate':cate,
        'data':data
        
        
    }
    return render(request,'main/index.html',context)
    
def about(request):
    return render(request,'main/about.html')

@login_required(login_url='log_in')
def menu(request):
    return render(request,'main/menu.html')
    
def service(request):
    return render(request,'main/services.html')

def contact(request):
    return render(request,'main/contact.html')

# ------------------------------authentication part ---------------------
def register(request):
    if request.method=='POST':
        data=request.POST
        fn=data['first_name'] #ram
        last_name=data['last_name']
        username=data['username'] #ram@gmail
        email=data['email']
        password=data['password']
        password1=data['password1']
        
        if password==password1:
            try:
                validate_password(password)
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username is already exists')
                    return redirect('register')
                
                if User.objects.filter(email=email).exists():
                    messages.error(request,'email is already exists')
                    return redirect('register')
                User.objects.create_user(first_name=fn,last_name=last_name,username=username,email=email,password=password)
                messages.success(request,'Your account successfully register!!!')
                return redirect('log_in')
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request,error)
                return redirect('register')
                    
                
        else:
            messages.error(request,"your password and confirm doesnot match!!!")
            return redirect('register')
            
        
        
    return render(request,'auth/register.html')

def log_in(request):
    if request.method=='POST':
        username=request.POST['username'] #ram710
        password=request.POST['password']
        remember_me=request.POST.get('remember_me') #None
        
        
        
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username is not register yet!!!")
            return redirect('log_in')
        
        user=authenticate(username=username,password=password)
        
        if user is not None:
            login(request,user)
            if remember_me:
                request.session.set_expiry(3600000)
            else:
                request.session.set_expiry(0)
            
            return redirect('index')
        
        else:
            messages.error(request,'Your password is invalid')
            return redirect('log_in')   
        

    return render(request,'auth/login.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

@login_required(login_url='log_in')
def change_password(request):
    form=PasswordChangeForm(user=request.user)
    
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
    return render(request,'auth/change_password.html',{'form':form})



#new change here 
print("hello this  is new file")