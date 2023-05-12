from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self,email,password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None):
        user = self.create_user(
            email,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    #팔로우, 다대다관계: 서로 참조 가능, 나뉘어 있을 필요 없고 User안에 있어도 됨, 
    #symmetric
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    bookmark = models.ManyToManyField('boards.Board', related_name="bookmarking_people", blank=True)
    likes = models.ManyToManyField('boards.Board', related_name="liking_people", blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property          #필수사항
    def is_staff(self):
        return self.is_admin

class Verify(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)