import uuid

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


def avatar_directory_path(instance, filename):
    return f'{settings.AVATAR_PATH}/{uuid.uuid4().hex}.jpg'

class UserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(
            email=email, 
            password=password,
            is_superuser=True,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, is_superuser=False):
        if not email:
            raise ValueError(_('Email is Required.'))
        if not password:
            raise ValueError(_('Password is Required.'))
        user = self.model(
            username=username,
            email=email,
            is_superuser=is_superuser
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICE = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    username     = models.CharField(max_length=255, null=True, unique=True, verbose_name=_('Username'))
    fullname     = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Full Name'))
    gender       = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICE, default=None, verbose_name=_('Gender'))
    dob          = models.DateField(null=True, blank=True, verbose_name=_('Date of Birth'))
    email        = models.EmailField(max_length=255, unique=True, verbose_name=_('Email'))
    score        = models.IntegerField(null=True, blank=True, verbose_name='Score')
    avatar       = models.ImageField(upload_to=avatar_directory_path, null=True, blank=True, verbose_name=_('Avatar'))
    created_at   = models.DateTimeField(verbose_name=_('Created At'), auto_now_add=True)
    is_superuser = models.BooleanField(default=False, verbose_name=_('Is Superuser?'))
    is_admin     = models.BooleanField(default=False, verbose_name=_('Is Admin?'))
    is_active    = models.BooleanField(default=True, verbose_name=_('Is Active?'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    class Meta:
        ordering = ('id',)
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email
        
    @property
    def is_staff(self):
        return self.is_admin or self.is_superuser

    @property
    def avatar_preview(self):
        if self.avatar:
            return mark_safe('<img src="{}" width="300" height="300" />'.format(self.avatar.url))
        return "-"