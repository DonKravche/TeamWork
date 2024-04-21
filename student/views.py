from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from .forms import StudentRegistrationForm, LoginForm
from .models import Student


def home(request):
    return render(request, 'home.html')


def login_page(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():

            Student.objects.create_user(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            # Student.objects.create(email=form.cleaned_data.get('email'), password=form.cleaned_data.get('password'))
            return JsonResponse({'message': 'Student registered successfully'})
    else:
        form = StudentRegistrationForm()
    return render(request, 'registration_form.html', {'form': form})


def login_(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'successful_login.html')
            else:
                return render(request, 'login.html', {'form': form})

        else:
            return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form})


def students_page(request):
    return render(request, 'successful_login.html')


def registration_student(request):
    return render(request, 'successful_registration.html')