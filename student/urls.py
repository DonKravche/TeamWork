from django.urls import path

from student import views
from student.views import register_student

urlpatterns = [
    path('home/', views.home, name='home'),
    path('register/', register_student, name='register_student'),
    path('login/', views.login_, name='login_')
]
