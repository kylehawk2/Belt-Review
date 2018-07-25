# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validation(self, postData):
        errors = {}
        if len(postData['name']) < 2:
            errors["name"] = "User name must be more than two characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Please enter in a valid email address!"
        if "@" not in postData['email'] or "." not in postData['email']:
            errors["email"] = "Email must contain an @ or ."
        if len(postData['password']) < 4:
            errors['password'] = "Password must be at least 4 characters long!"
        if postData['password'] != postData['cpassword']:
            errors['password'] = "Passwords do not match!"
        return errors
        

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    cpassword = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return self.name, self.email

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return self.title, self.author

class Review(models.Model):
    review = models.CharField(max_length=255)
    book = models.ForeignKey(Book, related_name="reviews")
    user = models.ForeignKey(User, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    