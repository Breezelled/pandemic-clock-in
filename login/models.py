from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, UserManager
from PIL import Image


# Create your models here.

class Org(models.Model):
    org_id = models.CharField(max_length=255, blank=True, null=True)
    org_name = models.CharField(unique=True, max_length=255, blank=True, null=True)
    org_designate_location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'org'


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.BigIntegerField(primary_key=True)
    user_name = models.CharField(max_length=255, blank=True, null=True)
    user_org = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True, unique=True)
    user_bind_num = models.CharField(max_length=50, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photo/%Y%m%d/', max_length=255, blank=True, null=True,
                                      default='default.png')
    gender = models.IntegerField(blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    user_uuid = models.CharField(max_length=255, blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True, default=0)
    realname = models.CharField(max_length=10, blank=True, null=True)

    last_login = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        managed = False
        db_table = 'user'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # 原有的save
        user = super(User, self).save(*args, **kwargs)
        # 固定宽度缩放
        if self.profile_photo and not kwargs.get('update_fields'):
            image = Image.open(self.profile_photo)
            (x, y) = image.size
            nx = 200
            ny = int(nx * (y / x))
            resized = image.resize((nx, ny), Image.ANTIALIAS)
            resized.save(self.profile_photo.path)

        return user


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("请填入邮箱！")
        if not password:
            raise ValueError("请填入密码!")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user = self._create_user(username=username, email=email, password=password)
        extra_fields.setdefault('is_superuser', True)

        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return user
