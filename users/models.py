import jwt

from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        # if not email:
        #     raise ValueError("Пожалуйста, введите email")
        # if not phone:
        #     raise ValueError("Пожалуйста, введите телефон")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('Владелец', 'Владелец'),
        ('Персонал', 'Персонал'),
        ('Клиент', 'Клиент')
    )
    name = models.CharField(verbose_name='Имя', max_length=64, null=True, blank=True)
    surname = models.CharField(verbose_name='Фамилия', max_length=64, null=True, blank=True)
    patronymic = models.CharField(verbose_name='Отчество', max_length=64, null=True, blank=True)
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    username = models.CharField(verbose_name='Телефон', max_length=64, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=64, unique=True)
    category = models.CharField(verbose_name='Категория пользователя', choices=USER_TYPES, max_length=64, blank=True,
                                null=True)
    is_admin = models.BooleanField(verbose_name='Администратор', default=False)
    is_staff = models.BooleanField(verbose_name='Персонал', default=False)
    is_active = models.BooleanField(verbose_name='Активен', default=True)
    is_superuser = models.BooleanField(verbose_name='Суперпользователь', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = MyUserManager()

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return '%s %s %s' % (
            self.name, self.surname, self.patronymic,
        )

    @property
    def token(self):
        return self._generate_jwt_token()

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')
