from django.db import models
import uuid


# Create your models here.

class site_admin(models.Model):
    gen = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('o', 'Other')
    ]
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    reg_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(max_length=200)
    gender = models.CharField(max_length=1, choices=gen, default=' ', )
    phone = models.CharField(max_length=20)
    object = models.Manager

    def __str__(self):
        return f"{self.name} Is A Admin"

    class Meta:
        db_table = "site_admin"
