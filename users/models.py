from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

from users.utils import create_avatar
from users.validators import validate_github_url


class UserManager(BaseUserManager):
    """Менеджер для создания пользователей через email"""
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # для вызова clean модели(там приводится телефон к единому формату)
        user.full_clean()
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=124)
    surname = models.CharField("Фамилия", max_length=124)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    phone = models.CharField("Телефон", max_length=12, unique=True, validators=[
        RegexValidator(
            regex=r"\A(?:8|\+7)[0-9]{10}\Z",
            message="Введите номер телефона в формате 8XXXXXXXXXX или +7XXXXXXXXXX.",
        ),
    ])
    github_url = models.URLField(
        "GitHub",
        blank=True,
        validators=[validate_github_url],
    )
    about = models.TextField("О себе", max_length=256, blank=True)
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Доступ в админку", default=False)
    date_joined = models.DateTimeField("Дата регистрации", default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    # Для создания через createsuperuser
    REQUIRED_FIELDS = ["name", "surname", "phone"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-date_joined", "-id"]

    def clean(self):
        super().clean()
        # Привожу телефон к единому формату - +7
        if self.phone and self.phone.startswith("8"):
            self.phone = "+7" + self.phone[1:]

    def save(self, *args, **kwargs):
        # Дефолтный аватар с первой буквой имени
        if not self.avatar:
            self.avatar = create_avatar(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname} ({self.email})"