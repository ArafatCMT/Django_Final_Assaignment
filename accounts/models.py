from django.db import models
from django.contrib.auth.models import User

# Create your models here.

GENDER = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]

RELATIONSHIP_STATUS = [
    ('Single', 'Single'),
    ('In a relationship', 'In a relationship'),
    ('Engaged', 'Engaged'),
    ('Married', 'Married'),
]

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='accounts/images/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_no = models.CharField(max_length=12, null=True, blank=True)
    gender = models.CharField(choices=GENDER, max_length=10, null=True, blank=True, default="Male") 
    city = models.CharField(max_length=30, null=True, blank=True)
    relationship = models.CharField(max_length=30, choices=RELATIONSHIP_STATUS, null=True, blank=True, default="Single")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"