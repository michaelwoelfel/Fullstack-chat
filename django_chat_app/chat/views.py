from django.shortcuts import render, redirect
from .models import Chat, Message
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from django.contrib.auth import logout
import json



"""
This is the function where you get after the login. The chat room where all messages are rendered.
"""
# Erstelle deine Views hier.
@login_required(login_url='/login/')  # Dekorator, der den Zugang zu dieser View auf eingeloggte Nutzer beschränkt
def index(request):
    if request.method == 'POST':  # Überprüft, ob die Anfrage eine POST-Anfrage ist
        print("Received Data" + request.POST['textmessage'])  # Gibt die empfangenen Daten in der Konsole aus
        myChat = Chat.objects.get(id=1)  # Holt den Chat mit der ID 1 aus der Datenbank
        # Erstellt eine neue Nachricht mit den Daten aus dem POST-Request
        new_message = Message.objects.create(text=request.POST['textmessage'], 
                                             chat=myChat, 
                                             author=request.user,
                                             receiver=request.user)
        message_data = model_to_dict(new_message)
       
        return JsonResponse({'model': 'chat.message', 'pk': new_message.pk, 'fields': message_data})
    chatMessages = Message.objects.filter(chat__id=1)  # Holt alle Nachrichten des Chats mit der ID 1
    # Gibt die index.html zurück und übergibt die Nachrichten
    
    return render(request, 'chat/index.html', {'messages': chatMessages})


"""
This is the login_view where you have a login mask to login or create a new user.
"""
def login_view(request):
    redirect = request.GET.get('next', '/chat/')  # Holt den 'next' Parameter aus dem GET-Request oder setzt '/chat/' als Standard
    if request.method == 'POST':  # Überprüft, ob die Anfrage eine POST-Anfrage ist
        # Authentifiziert den Nutzer basierend auf Username und Passwort
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)  # Loggt den Nutzer ein
            print('redirect', redirect)  # Gibt den Redirect-Pfad in der Konsole aus
            return HttpResponseRedirect(request.POST.get('redirect'))  # Leitet den Nutzer an den gewünschten Pfad weiter
        else:
            # Gibt das Login-Template mit einer Fehlermeldung zurück
            return render(request, 'login/login.html', {'wrongPassword': True, 'redirect': redirect})
    # Gibt das Login-Template zurück, falls keine POST-Anfrage vorliegt
    return render(request, 'login/login.html', {'redirect': redirect})



"""
This is the create_User view where a new user can be created.
"""
def createUser_view(request):
    context = {}  # Initialisiert einen Kontext-Dictionary
    if request.method == 'POST':  # Überprüft, ob die Anfrage eine POST-Anfrage ist
        username = request.POST.get('newUser')  # Holt den Benutzernamen aus dem POST-Request
        password = request.POST.get('newPassword')  # Holt das Passwort aus dem POST-Request
        password_validation = request.POST.get('newPasswordValidation')  # Holt die Passwort-Validierung aus dem POST-Request
        if password != password_validation: 
             context['password_error'] = "Passwörter stimmen nicht überein"
        else:
             # Überprüfen, ob der Benutzername bereits existiert
          if User.objects.filter(username=username).exists():
                context['username_error'] = "Benutzername bereits vergeben"
          else:
           User.objects.create_user(username=username, password=password) 
           return redirect('/login/') 
    # Gibt das createUser-Template zurück
    return render(request, 'createUser/createUser.html', context)


def logout_view(request):
    logout(request)
    return redirect('/login/')