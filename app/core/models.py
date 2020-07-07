from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):  # **allows
        # length of arguments to be passed
        '''Creates and saves a new user. this is custom manager for
        User model, objects = UserManager() ties the two together'''
        if not email:
            raise ValueError('Users must have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  # to support multiple db

        return user

    def create_superuser(self, email, password):  # password cannot be null for superuser
        '''Create and save a new superuser with given details'''
        user = self.create_user(email, password)  # calls create_user method, here self is not specified as arg since it is passed automatically when function/method (create_user in this case) is called

        user.is_superuser = True  # is_superuser is automatically created by PermissionsMixin base class
        user.is_staff = True  # is_staff is specified in the UserProfile class
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''Custom user model that supports using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)  # models is impor
    # on first line
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # UserManager is assigned to objects attribute

    USERNAME_FIELD = 'email'
