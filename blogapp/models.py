from django.db import models
from django.contrib.auth.models import User as user

class User(models.Model):
    full_name=models.CharField(max_length=50)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField('date')
    author = models.ForeignKey("User", on_delete=models.CASCADE, related_name="blog")
    
    def __str__(self):
        return str(self.title)+" by "+str(self.author)+ " at: "+str(self.date)[4:]
    class Meta:
        ordering=['-id']
        
    