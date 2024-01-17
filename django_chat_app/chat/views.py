from django.shortcuts import render
from .models import Chat, Message
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

#Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("Received Data" + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat,author=request.user,receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1)   
    return render(request, 'chat/index.html', {'messages':chatMessages})

def login_view(request):
    redirect = request.GET.get('next', '/chat/')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            print('redirect',redirect)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'login/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'login/login.html', {'redirect': redirect})
                  
def createUser_view(request):
    return render(request,'createUser/createUser.html')