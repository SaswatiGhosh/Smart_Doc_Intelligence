from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import os

def login_view(request):
    if request.method=="POST":
        user=authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request,user)
            return redirect('upload')
    return render(request, 'login.html')


# @login_required

def upload_view(request):
    if request.method=="POST":
        file=request.FILES['file']
        print(file)
        file_path=os.path.join('uploads/', file.name)
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return redirect('chat')
    return render(request ,'upload.html')

# @login_required

def chat_view(request):
    return render(request, 'chat.html')

            






