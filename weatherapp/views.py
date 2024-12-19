from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import requests
import datetime
from django.contrib.auth.decorators import login_required
import os
from dotenv import load_dotenv
load_dotenv()



# login,logout
# User model
def signupview(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user_name=request.POST.get('user_name')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already exist')
        if password ==confirm_password:
            user=CustomUser.objects.create_user(email=email,username=user_name)
            user.set_password(password)
            user.save()
            return redirect('signin')
        return redirect('signup')
    return render(request,'signup.html')

def signinview(request):
    if request.method=='POST':
        try:
            user_name=request.POST.get('username')
        except:
            messages.error(request,'Invalid Username...Please enter a valid username')
        password=request.POST.get('password')
        user=authenticate(username=user_name,password=password)
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('signin')
        else:
            login(request, user)
            return redirect('home')
        # try:
        #     user=User.objects.get(username=user_name)
        #     print(user,'uuuuuuuuuuuuuu')
        # except:
        #     User.DoesNotExist
        #     messages.error(request, 'User does not exist')
        #     redirect('signin')
        # print('authenticting')
        # if user.password==password:
        #     print('authenticted')
        # print(user)
        # if user:
        #     messages.success(request, 'Login successfull')
        #     return redirect('home')
        # else:
        #     messages.error(request, 'Incorrect password')
    return render(request,'signin.html')

def homeview(request):
    user=request.user
    # print('user',request.user)
    return render(request,'home.html',{'user':user})
def signoutview(request):
    logout(request)
    messages.success(request,'You have been logged out succesfully')
    return redirect('signin')

@login_required(login_url='signin')
def weather(request):
    if 'city' in request.POST:
        city = request.POST.get('city')
    else:
        city = 'calicut'
    
    APP_ID = os.getenv('APP_ID')
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APP_ID}"
    PARAMS = {'units': 'metric'}

    try:
        data=requests.get(url,params=PARAMS).json()
        description = data['weather'][0]['description']
        icon=data['weather'][0]['icon']
        temp=data['main']['temp'] 
        day=datetime.date.today()

        context ={
            'description': description,
            'icon':icon,
            'temp':temp,
            'day': day,
            'city': city,
            'exception_occurred':False
        }
        return render(request,'weather.html',context)
              
    except KeyError:
        exception_occurred=True
        messages.error(request,'Enter data is not available to API')
        day=datetime.date.today()
    return render(request,'weather.html',{
        'description':'clear sky',
        'icon':'0ld',
        'temp':25,
        'day': day,
        'city':'calicut',
        'exception_occurred':exception_occurred,
    })
