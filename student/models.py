from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=255, verbose_name="Faculty name")

    def __str__(self):
        return self.name


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Subject Name")
    description = models.TextField(verbose_name="Subject Description")
    syllabus = models.FileField(upload_to='syllabi/', verbose_name="Syllabus")
    faculties = models.ManyToManyField(Faculty, related_name='subjects')
    lecturers = models.ManyToManyField('Lecture', related_name='subjects')

    def __str__(self):
        return self.title


class Lecture(models.Model):
    name = models.CharField(max_length=255, verbose_name="Lecture Name")
    surname = models.CharField(max_length=255, verbose_name="Lecture Surname")

    def __str__(self):
        return f"{self.name} {self.surname}"


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = email.lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Student(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="Student Name")
    surname = models.CharField(max_length=255, verbose_name="Student Surname")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    subjects = models.ManyToManyField(Subject, verbose_name='subjects')
    email = models.EmailField(max_length=255, verbose_name="Student Email", unique=True)
    password = models.CharField(max_length=255, verbose_name="Student Password")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()
    username = None

    def __str__(self):
        return f"{self.name} {self.surname}"

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False
