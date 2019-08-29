from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='/userprofile/login') 
def User_delete(request, id):
    user = User.objects.get(id=id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect('index')
    else:
        return HttpResponse('You do not have the Permission to do that！')

def User_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)

        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('index')
        else:
            return HttpResponse('Please check you register information!')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('Lack of POST or GET method in your request!')


def User_logout(request):
    logout(request)
    return redirect('index')

def User_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Please check your name and password!')
        else:
            return HttpResponse('Your name or password is not valid!')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('Lack of POST or GET method in your request!')


