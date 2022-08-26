from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
import sqlite3
import datetime

@login_required
def homePageView(request):
	messages = Message.objects.filter(Q(source=request.user) | Q(target=request.user)).order_by('time')
	users = User.objects.all()
	return render(request, 'poster/home.html', {'msgs': messages, 'users': users})

@login_required
def sendView(request):
    source = request.user
    target = User.objects.get(username=request.POST.get('to'))
    content = request.POST.get('content')

    source_id = source.id
    target_id = target.id
    time = str(datetime.datetime.now())

    # Flaw 2: SQL injection
    # -----------------------------------
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.executescript('INSERT INTO poster_message (content, time, source_id, target_id) VALUES (\'%s\', \'%s\', %s, %s)' % (content, time, source_id, target_id))

    # Fix for flaw 2 option 1: use execute() that allows only one statement to be executed at a time, and a parameterized SQL statement
    # cursor.execute('INSERT INTO poster_message (content, time, source_id, target_id) VALUES (:content, :time, :source_id, :target_id)', {'content': content, 'time': time, 'source_id': source_id, 'target_id': target_id})
    
    conn.commit()
    conn.close()

    # -----------------------------------
    # Fix for flaw 2 option 2: delete lines 28-37 and use models!
    # Message.objects.create(source=source, target=target, content=content)

    return redirect('/')

@login_required
def deleteView(request, message_id):
    message = Message.objects.get(pk=message_id)
    # Flaw 1:
    # ---------------
    message.delete()
    # ---------------
    # Flaw 1 Fix:
    # instead of directly deleting check that the user is the owner of the message
    # if (message.source == request.user or message.target == request.user):
    #     message.delete()
    return redirect('/')