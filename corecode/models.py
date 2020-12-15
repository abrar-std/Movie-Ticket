from django.db import models
import uuid
from django.urls import reverse

# Create your models here.

class user(models.Model):
    gen = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Other')
    ]
    status = [
        ('A', 'approved'),
        ('P', 'pending'),
        ('B', 'blocked')
    ]
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=200)
    gender = models.CharField(max_length=1, choices=gen, default=' ', )
    phone = models.CharField(max_length=20)
    user_status = models.CharField(max_length=1, choices=status, default='P', )
    object = models.Manager

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user"

    def get_absolute_url(self):
        return reverse("index")
