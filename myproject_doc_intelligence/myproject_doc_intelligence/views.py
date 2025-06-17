from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .utils import sns_invoking_summary
from .utils.s3_upload import upload_file_to_s3
import os


def home_view(request):
    return redirect("upload")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            print("Here")
            messages.success(request, f"Welcome back, {username}!")
            return redirect("upload")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")

    return render(request, "login.html")


def no_user_found_view(request):
    return redirect("login")


def logout_view(request):
    logout(request)
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect("signup")

        # Create the user
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "signup.html")


"""
This method is to edit the name of the file that is being uploaded.
Files having anything apart from alphanumeric chars, dots and underscore were not working.
Textract were not picking up the file name
"""


def fileNameEdit(name):
    name = name.lower()
    editedName = ""
    c = 0
    for i in name:
        if c > 15:
            break
        if 97 <= ord(i) <= 122 or 48 <= ord(i) <= 57:
            editedName += i
        else:
            editedName += "_"
        c += 1
    return editedName


@login_required
def upload_view(request):
    if request.method == "POST":
        file = request.FILES["file"]
        file_name = file.name
        file_extension = file_name[file_name.rfind(".") :]

        file_content_type = file.content_type

        file_name = fileNameEdit(file.name) + file_extension
        print(request.user)
        user_name = str(request.user) if request.user.is_authenticated else "anonymous"
        file_path = os.path.join("uploads/", user_name + "_" + file_name)

        file_name = user_name + "_" + file_name
        settings.FILE_NAME = file_name

        with open(file_path, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        if upload_file_to_s3(file_path, file_name, file_content_type):
            return redirect("chat")

    return render(request, "upload.html")


@login_required
def chat_view(request):
    context = {}
    if settings.FILE_NAME == "":
        return redirect("upload")

    if request.method == "POST":
        message = request.POST.get("message", "")
        action = request.POST.get("action")
        model_response = sns_invoking_summary.sns_invoking_summary(action, message)
        context = {"messages": model_response}
    return render(request, "chat.html", context)
