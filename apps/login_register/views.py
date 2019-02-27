from django.shortcuts import render, redirect
from .models import User, UserManager
from django.contrib import messages
import bcrypt

def show_login(request):
    request.session.clear()

    return render(request, 'login_register/login.html')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if errors != None:
        for tag, message in errors.items():
            messages.error(request, message, extra_tags = tag)
            
        return redirect('/')
    if errors == None:
        user = User.objects.filter(email = request.POST['login_email'])
        request.session['first_name'] = user[0].first_name
        request.session['user_id'] = user[0].id

        return redirect('/success')

def show_registration(request):
    request.session.clear()

    return render(request, 'login_register/register.html')

def register_user(request):
    response = User.objects.registration_validator(request.POST)
    print(response)
    if response[0] != True:
        for tag, message in response[1].items():
            messages.error(request, message, extra_tags = tag)
        return redirect('/signup')

    if response[0] == True:
        request.session['user_id'] = response[1].id
        request.session['first_name'] = response[1].first_name
        return redirect('/success')

def success(request):
    return redirect('/trips')
