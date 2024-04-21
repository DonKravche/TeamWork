from django.urls import path

from student import views
from student.views import register_student, registration_student, login_, students_page

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', register_student, name='register_student'),
    path('login/', login_, name='login_'),
    path('login/students_page/', students_page, name='students_page'),
    path('register/registration_page/', registration_student, name='registration_student'),
]
