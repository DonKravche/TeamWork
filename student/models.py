from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser


# Create your models here.
class Faculty(models.Model):
    name = models.CharField(verbose_name="Faculty name", max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Faculties'
        verbose_name = 'Faculty'


class Lecturer(models.Model):
    name = models.CharField(verbose_name="Lecturer Name", max_length=255)
    surname = models.CharField(verbose_name="Lecturer Surname", max_length=255)

    def __str__(self):
        return f"{self.name} {self.surname}"

    class Meta:
        verbose_name_plural = 'Lecturers'
        verbose_name = 'Lecturer'


class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="Subject Name", max_length=255)
    description = models.TextField(verbose_name="Subject Description")
    syllabus = models.FileField(verbose_name="Syllabus", upload_to='syllabuses/')
    faculties = models.ManyToManyField(Faculty, related_name='subjects')
    lecturers = models.ManyToManyField(Lecturer, related_name='subjects')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Subjects'
        verbose_name = 'Subject'


class UserManager(BaseUserManager):
    def _create_user(self, name, surname, email, password, **extra_fields):
        name = name.lower()
        surname = surname.lower()
        email = email.lower()
        user = self.model(name=name, surname=surname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, surname, email, password=None, **extra_fields):
        name = name.lower()
        surname = surname.lower()
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, surname, email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Student(AbstractUser):
    name = models.CharField(verbose_name="Student Name", max_length=255)
    surname = models.CharField(verbose_name="Student Surname", max_length=255)
    email = models.EmailField(verbose_name="Student Email", max_length=255, unique=True)
    password = models.CharField(verbose_name="Student Password", max_length=255)
    faculty = models.ForeignKey(
        Faculty,
        verbose_name="Faculty",
        on_delete=models.CASCADE,
        related_name='students',
        null=True,
        blank=True
    )
    subjects = models.ManyToManyField(
        Subject,
        verbose_name='Subjects',
        related_name='students',
        blank=True
    )
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

    class Meta:
        verbose_name_plural = 'Students'
        verbose_name = 'Student'
