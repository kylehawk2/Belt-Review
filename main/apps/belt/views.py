# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import User, UserManager
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'belt/index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.validation(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            print "Its working"
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], email=request.POST['email'], password=hash1)
            messages.error(request, 'Registration Successful')
        return render(request, 'belt/home.html')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        messages.error(request, "Invalid User")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode()) ):
            print "Password matches"
            request.session['id'] = user[0].id
            return redirect('/home')
        else:
            messages.error(request, "Invalid Password")
            return redirect('/')

def home(request):
    context = {
        'users' : User.objects.get(id=request.session['id'])
    }
    return render(request, 'belt/home.html', context)

def bookreview(request):
    return render(request, 'belt/review.html')
    