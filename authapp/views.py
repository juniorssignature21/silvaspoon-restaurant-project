from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
import random

# Create your views here.
def index(request):
    return render(request, "index.html")

def register_user(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pswd = request.POST.get("pswd")
        cpswd = request.POST.get("cpswd")
        
        if cpswd != pswd:
            messages.info(request, "Passwords does not match!!!")
            return redirect('/auth/register')
        
        # add @ and numbers to username
        
        # generate a list of random numbers
        random_numbers = [random.randint(1,9) for _ in range(5)] # generate 5 random numbers
        
        # convert the list of numbers into a string
        output = ''.join(map(str, random_numbers))
        
        username = fname + "@" + output
        
        try:
            if User.objects.get(email=email):
                messages.warning(request, f"{email} have been used \n Try another email")
                return redirect('/auth/register')
        except Exception as identifier:
            pass
        
        myuser = User.objects.create_user(
            username,
            fname,
            lname,
            email,
            pswd
        )
        myuser.save()
        
        myuser = authenticate(email=email, password=pswd)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request, f"Hello {username} \n Welcome to silvaspoon!!!")
            return redirect('/')
        return redirect('/auth/register')
    return render(request, "authapp/register.html")

        