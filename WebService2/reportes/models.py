from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    is_staff = models.CharField(max_length=1, default='S')

    def __str__(self):
        return self.username