from django.shortcuts import render
from .models import Chat, Message
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login

#Create your views here.

def index(request):
    if request.method == 'POST':
        print("Received Data" + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat,author=request.user,receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1)   
    return render(request, 'chat/index.html', {'messages':chatMessages})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect('/chat/')
        else:
            return render(request, 'login/login.html', {'wrongPassword': True})
    return render(request, 'login/login.html')
                  
