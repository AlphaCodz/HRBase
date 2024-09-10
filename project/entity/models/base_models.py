from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid, enum, random, string


class CustomUserManager(BaseUserManager):
    def create_user(self, contact, password=None, **extra_fields):
        if not contact:
            raise ValueError('The Contact field must be set')
        user = self.model(contact=contact, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, contact, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(contact, password, **extra_fields)

# Create your models here.
class Role(models.TextChoices):
    USER = "USER", "User"
    ORG_ADMIN = "ORG_ADMIN", "Organization Admin"
    ORG_STAFF = "ORG_STAFF", "Organization Staff"
    ORG_HR = "ORG_HR", "HR Representative"
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    

class User(AbstractUser):
    ROLES = (
        ("USER", "User"),
        ("ORG_ADMIN", "Organisation Admin"),
        ("ORG_STAFF", "Organisation Staff"),
        ("ORG_HR", "HR Representative"),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=350, null=False, blank=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default="USER")
    address = models.CharField(max_length=300, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.TimeField(auto_now=True)
    username = models.CharField(max_length=7, null=True)
    
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.password:
            self.set_password(self.password)
        if not self.username:
            self.username = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
        super(User, self).save(*args, **kwargs)