from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    
    title= models.CharField(max_length=255)
    content=models.TextField()
    photo = models.ImageField(upload_to="images")
    video = models.FileField(upload_to="videos")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
   

    def __str__(self):
        return self.title
    
    
        
