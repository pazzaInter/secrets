# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import Count
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Secret, Like, User

def welcome(request):
    if 'user' in request.session:
        print "Logged in user is", request.session['user']['name']
        user = User.objects.get(email = request.session['user']['email'])
        secrets = Secret.objects.recent()
        context = {
            'user': user,
            'secrets': secrets,
        }
        return render(request, 'secrets/index.html', context)
    return redirect('login:index')

def post_secret(request):
    if request.method == 'POST':
        print 'Attempting to check and then add secret by User Email'
        posted = Secret.objects.new_secret(request.POST['secret'], request.session['user']['email'])
        if posted:
            print 'Success, the secret was posted'
            return redirect('secrets:welcome')
        elif not posted:
            print 'Did not post'
            messages.add_message(request, messages.ERROR, 'Please post a message.')
            return redirect('secrets:welcome')
    return redirect('secrets:welcome')

def popular(request):
    user = User.objects.get(email = request.session['user']['email'])
    secrets = Secret.objects.popular()
    context = {
        'user': user,
        'secrets': secrets,
    }
    return render(request, 'secrets/popular.html', context)

def like(request, id):
    liked = Like.objects.liked(request.session['user']['email'],id)
    print 'Liked'
    return redirect('secrets:welcome')

def delete(request, id):
    secret = Secret.objects.get(id = id)
    print secret
    deleted = secret.delete()
    print deleted
    return redirect('secrets:welcome')
