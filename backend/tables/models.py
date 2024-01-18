from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.validators import MinLengthValidator
from django.db import models

from .validators import numeric_only, validate_telephone_number


class UserManager(BaseUserManager):
    """Класс для управления создания и обработки пользователей."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Требуется ввести Email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        'Адрес электронной почты',
        max_length=70,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=40,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=40,
    )
    phone_number = models.CharField(
        validators=[validate_telephone_number],
        max_length=17,
        blank=True
    )
    organization = models.ForeignKey(
        'Organization',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='employee'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.email}'


class Organization(models.Model):
    """Модель организации."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    address = models.CharField(max_length=200)
    postcode = models.CharField(
        max_length=6,
        validators=[MinLengthValidator(6), numeric_only]
    )

    def __str__(self):
        return f'{self.title}'


class Event(models.Model):
    """Модель мероприятия."""

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    organizations = models.ManyToManyField(Organization)
    image = models.ImageField(blank=True, null=True, upload_to='images')
    date = models.DateTimeField()

    def __str__(self):
        return f'{self.title} in {self.date}'
