from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
  
def registerView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/')
        messages.error(request, 'Unsuccessful registration. Invalid information.')

    form = UserCreationForm()

    return render (request=request, template_name='poster/register.html', context={'form':form})