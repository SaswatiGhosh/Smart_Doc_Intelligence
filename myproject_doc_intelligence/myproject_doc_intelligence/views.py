from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .utils.s3_upload import upload_file_to_s3
import os


def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("upload")
    return render(request, "login.html")


# @login_required


def upload_view(request):
    if request.method == "POST":
        file = request.FILES["file"]
        file_name = file.name
        file_content_type = file.content_type
        print(file)
        user_id = request.user.id if request.user.is_authenticated else "anonymous"
        file_path = os.path.join("uploads/", user_id + file_name)
        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        if upload_file_to_s3(file_path,user_id+ "_" + file_name, file_content_type):
            
            return redirect("chat")
        
    return render(request, "upload.html")


# @login_required


def chat_view(request):
    return render(request, "chat.html")
