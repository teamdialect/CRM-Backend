from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    mobile_number = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.username
    
class Lead(models.Model):    
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    lead_description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=[
        ('new', 'New'),
        ('qualifying', 'Qualifying'),
        ('proposal', 'Proposal'),
        ('negotiating', 'Negotiating'),
        ('archive', 'Archive')
    ], default='new')

    def __str__(self):
        return self.name
    
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    checklists = models.JSONField(default=list)

    def __str__(self):
        return self.name 