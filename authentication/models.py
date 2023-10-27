from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import validate_email
from shortuuidfield import ShortUUIDField


# User authentication information
class UserAccountManager(BaseUserManager):

    def create_user(self, email, password=None):

        if not email:
            raise ValueError("Email field is required")

        email = self.normalize_email(email)
        user = self.model(email=email)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)

        user.is_admin = True
        user.save(using=self._db)
        return user


class Image(models.Model):
    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    image = models.ImageField(upload_to="profile/")


class UserAccount(AbstractBaseUser,PermissionsMixin):
    id = ShortUUIDField(primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True, max_length=50,validators=[validate_email])
    name = models.CharField(max_length=100, null=True,blank=True)
    profile_image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    otp = models.CharField(max_length=4)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.IntegerField(default=5)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
