from django.shortcuts import render

#Create your views here.

def index(request):
    if request.method == 'POST':
        print("Received Data" + request.POST['textmessage'])
    return render(request, 'chat/index.html')
