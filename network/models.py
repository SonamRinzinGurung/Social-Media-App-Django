from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Posts(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.post} --> {self.created_by}"
    
    
class Likes(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='liked_post')
    
    def __str__(self):
        return f"{self.liked_by} liked {self.liked_post}"
    
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    
    def __str__(self):
        return f'{self.follower} is following {self.following}'