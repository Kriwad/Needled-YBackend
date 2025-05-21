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
    
    

class PostsList(models.Model):

  title = models.CharField( max_length=30,  blank = True, null = True )
  content = models.TextField( blank = True , null=True)
  created_at = models.DateTimeField( default=timezone.now)
  user = models.ForeignKey(CustomUser , on_delete=models.CASCADE ,related_name = "postlist" )

  def __str__(self):
    return self.title or f"PostsList {self.id}" or "Untitled PostsList"

  def save(self , *args , **kwargs):
     self.clean()
     super(PostsList , self).save(*args , **kwargs)

   
class PostsImage(models.Model):
  post = models.ForeignKey(PostsList , on_delete= models.CASCADE , related_name="images" , null = True , blank=True)
  image = models.ImageField(upload_to='postImage' , null = True , blank= True)

class PostsVideo(models.Model):
  post = models.ForeignKey(PostsList , on_delete= models.CASCADE , related_name = "videos" )
  video = models.FileField(upload_to = "postVideos", null=True,blank = True)

class Like(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  post = models.ForeignKey(PostsList , on_delete= models.CASCADE  , null= True)
  created_at = models.DateTimeField(default=timezone.now)

  class Meta : 
    unique_together = ["user" , "post"]# Prevent multiple likes from same user
  
class Comment(models.Model):
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  post = models.ForeignKey(PostsList , on_delete= models.CASCADE , null = True  , blank=True )
  commentcontent = models.TextField()
  created_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
      return f"Comment by {self.user.username} on {self.post.title} "
    