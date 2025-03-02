from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.


class CustomUser(AbstractUser):
    
   
    middle_name = models.CharField(max_length=15, null = True , blank=True)
    image = models.ImageField(upload_to="Profilepictures" , blank= True )
    bio = models.CharField(max_length= 75 , blank=True , null = True)
    fullname = models.CharField(max_length=30 , blank = True , null = True )
    groups = models.ManyToManyField('auth.Group', related_name='user_set_api', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_set_api', blank=True)

    def save(self , *args , **kwargs):
      self.fullname = f"{self.first_name} {self.last_name}".strip()
      super().save(*args , **kwargs)

    def __str__(self):
        return self.username
    
    
   

class ToDoList(models.Model):

  title = models.CharField( max_length=30,  blank = True , null = True )
  goal = models.TextField( blank = True , null = True)
  image = models.ImageField( upload_to='todoImage',null = True , blank=True,)
  video= models.FileField(upload_to="todoVideos" , null = True , blank= True )
  created_at = models.DateTimeField( default=timezone.now)
  user = models.ForeignKey(CustomUser , on_delete=models.CASCADE ,related_name = "todolist" ,null = True)

  def __str__(self):
    return self.title or f"TodoList {self.id}" or "Untitled TodoList"
  
  def clean (self):
      if not any (self.title or self.goal or self.image or self.video):
        raise ValidationError("You must provide atleast one of the following") 

  def save(self , *args , **kwargs):
     self.clean()
     super(ToDoList , self).save(*args , **kwargs)


class Like(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  todo = models.ForeignKey(ToDoList , on_delete= models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)

  class Meta : 
    unique_together = ["user" , "todo"]# Prevent multiple likes from same user
  
class Comment(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  todo = models.ForeignKey(ToDoList , on_delete= models.CASCADE)
  content = models.TextField()
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
      return f"Comment by {self.user.username} on {self.todo.title} "
    