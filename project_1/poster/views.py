from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q

@login_required
def homePageView(request):
	messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user)).order_by('time')
	users = User.objects.all()
	return render(request, 'poster/home.html', {'msgs': messages, 'users': users})

@login_required
def sendView(request):
    target = User.objects.get(username=request.POST.get('to'))
    Message.objects.create(source=request.user, target=target, content=request.POST.get('content'))
    return redirect('/')