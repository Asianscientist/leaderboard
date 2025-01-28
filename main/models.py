from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()



class GamesModel(models.Model):
    name=models.CharField(max_length=200)   
    description=models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    