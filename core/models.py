from django.db import models  
from datetime import datetime
from django.contrib.auth.models import User


class Mood(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=100)

    class Meta:
        db_table = "mood"
