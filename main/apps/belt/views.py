# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from models import User, Book, Review, UserManager
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
        
        return render(request, 'belt/home.html', { 'users' : User.objects.get(id=request.session['id']) })

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
            request.session['email'] = email
            return redirect('/home')
        else:
            messages.error(request, "Invalid Password")
            return redirect('/')

def home(request):
    context = {
        'users' : User.objects.get(id=request.session['id']),
        'review' : Review.objects.all().order_by('-created_at')[:3],
        'books' : Book.objects.all()
    }
    return render(request, 'belt/home.html', context)

def bookreview(request):
    context = {
        'users': User.objects.get(id=request.session['id'])
    }
    return render(request, 'belt/review.html', context)

def add_book(request):
    if request.POST['select'] != 'none':
        r = Book.objects.get(title=request.POST['select'])
        Review.objects.create(review = request.POST['review'], book=Book.objects.get(id = r.id), user = User.objects.get(email=request.session['email']))
       
    else:
        # print request.POST
        
        r = Book.objects.create(title=request.POST['title'], author=request.POST['author'])
        Review.objects.create(review=request.POST['review'], book=Book.objects.get(id = r.id), user = User.objects.get(email=request.session['email']))
    return redirect('/home')

def new_review(request, id):
    print "*" * 80
    Review.objects.create(review=request.POST.get('review'), book=Book.objects.get(id=request.POST['id']), user=request.session['email'])
    return redirect('/book/' + str(id))

def book(request, id):
    print "*" * 80
    if len(request.session['email']) < 1:
        return redirect('/')
    context = {
        'book': Book.objects.get(id=id),
        'review': Review.objects.filter(book=Book.objects.get(id=id)).order_by("-created_at")
    }
    return render(request, 'belt/books.html', context)

def user(request, id):
    context = {
        'user' : User.objects.get(id=id),
        'review': Review.objects.filter(user=User.objects.get(id=id)).order_by('-created_at'),
        'review_count': Review.objects.filter(user = User.objects.get(id=id)).count()
    }
    return render(request, 'belt/user.html', context)

def logout(request):
    request.session['email'] = ""
    return redirect('/')