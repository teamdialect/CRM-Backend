from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    profile_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.username
    
class Lead(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None, null=True)    
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('qualifying', 'Qualifying'),
        ('proposal', 'Proposal'),
        ('negotiating', 'Negotiating'),
        ('archive', 'Archive')
    ], default='new')

    def __str__(self):
        return self.name