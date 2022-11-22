from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self, email, handle, name, password=None):
        if not email:
            raise ValueError('User must have a valid email.')

        user = self.model(
            email=self.normalize_email(email),
            handle=handle,
            name=name
        )

        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.is_admin = False
        user.save(using=self.db)
        return user

    def create_superuser(self, email, handle, password, name):
        user = self.create_user(
            email=email,
            handle=handle,
            password=password,
            name=name
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):

    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    handle = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['handle', 'name']

    def __str__(self):
        return f'{self.handle}, {self.date_joined}, {self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


