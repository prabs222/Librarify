from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_librarian = models.BooleanField(default=False)
    has_borrowed = models.BooleanField(default=False)
     
    def __str__(self) -> str:
        return self.username
    
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
