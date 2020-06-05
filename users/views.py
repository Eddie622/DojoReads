from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def createUser(request):
    if request.method == "GET":
        return redirect("/")
    
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password = request.POST['pwd']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        User.objects.create(name=request.POST['name'],alias=request.POST['alias'],
        email=request.POST['email'],password=pw_hash)
        messages.success(request, "Account Created")
        return redirect("/")

def login(request):
    if request.method == "GET":
        return redirect("/")
    
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]

        if bcrypt.checkpw(request.POST['pwd'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('../books/')

    messages.error(request,'invalid email/password')
    return redirect("/")

def books(request):

    context = {
        'this_user' : User.objects.get(id=request.session['userid']),
        'all_users' : User.objects.all()
    }

    return render(request, 'dojoRead.html', context)
