from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class Category(models.Model):
    name = models.CharField(verbose_name='Категория пользователя', max_length=64)

    class Meta:
        verbose_name = "Категория пользователя"
        verbose_name_plural = "Категории пользователей"

    def __str__(self):
        return self.name


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


class MyUser(AbstractBaseUser):
    name = models.CharField(verbose_name='Имя', max_length=64, null=True, blank=True)
    surname = models.CharField(verbose_name='Фамилия', max_length=64, null=True, blank=True)
    patronymic = models.CharField(verbose_name='Отчество', max_length=64, null=True, blank=True)
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    username = models.CharField(verbose_name='Телефон', max_length=64, unique=True)
    email = models.EmailField(verbose_name='Email', max_length=64, unique=True)
    category = models.ForeignKey(
        Category, verbose_name='Должность', on_delete=models.CASCADE, default=None, null=True, blank=True
    )
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

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

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
