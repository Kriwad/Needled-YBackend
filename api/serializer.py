
# from .models import Posts
from rest_framework import serializers
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser , PostsList , Like  , Comment , PostsImage , PostsVideo , CommentLike

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields =['id', 'username', 'password', 'email', 'first_name', 'middle_name', 'last_name', 'fullname', 'image' ]
    extra_kwargs = {'password': {'write_only': True}}
  
  def validate_username(self, value):
    if CustomUser.objects.filter(username= value).exists():
      raise serializers.ValidationError("username is already taken.")
    return value
  
  def validate_password(self , value):
    if len(value)<8 :
      raise serializers.ValidationError("Password must be atleast greater than 8 characters")
    
    if not re.search(r"[A-Z]", value):
      raise serializers.ValidationError("Password must contain at least one uppercase letter ")
    
    if not re.search(r"[a-z]" , value):
      raise serializers.ValidationError("Password must contain atleast one lowercase letter")

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
    try: 
      print("Validating password...")
      validate_password(value)
    except Exception as e:
      print("Validation error:", e)
      raise serializers.ValidationError(str(e))
    return value


  def create(self, validated_data):
    print("Creating user with:", validated_data)
    user = CustomUser.objects.create_user(
      username = validated_data['username'],
      password = validated_data['password'],
      email=validated_data.get('email', ''),
      first_name=validated_data.get('first_name', ''),
      middle_name=validated_data.get('middle_name', ''),
      last_name=validated_data.get('last_name', ''),
    
    )
    
    return user  


class DetailUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'username'  , "first_name" , 'middle_name', "last_name" , 'fullname' , 'image', 'bio' ]

class PostsImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostsImage
    fields = ['id' , 'image']

class PostsVideoSerializer(serializers.ModelSerializer):
  class Meta:
    model= PostsVideo
    fields= ['id' , 'video']

class PostsSerializer(serializers.ModelSerializer):
  user = DetailUserSerializer( read_only = True)
  images = PostsImageSerializer(many = True , read_only = True)
  videos = PostsVideoSerializer(many= True ,read_only = True )
  like_count = serializers.SerializerMethodField()
  is_liked = serializers.SerializerMethodField()
  comment_count = serializers.SerializerMethodField()
  class Meta:
    model= PostsList
    fields = ['user' ,'id', 'title' , 'content' , 'images', 'videos', 'created_at' , 'like_count' , 'is_liked' , 'comment_count']
    read_only_fields = ['user']
  
  def get_like_count(self , obj):
    return Like.objects.filter(post = obj).count()
  
  def get_comment_count(self , obj):
    return Comment.objects.filter(post = obj).count()
  
  def get_is_liked(self , obj):
    user = self.context.get("request").user
    if user.is_authenticated:
      return Like.objects.filter(user = user , post= obj).exists() 
    return False

#like and comment

class LikeSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only = True)
  post = serializers.PrimaryKeyRelatedField(queryset = PostsList.objects.all())
  class Meta:
    model = Like
    fields = ["id" , "user" ,"post",  "created_at"]

class CommentUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ["id" , "username" ,"fullname",  "image"]

class CommentSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only  = True)
  comment_like_count = serializers.SerializerMethodField()
  is_comment_liked = serializers.SerializerMethodField()

  def get_comment_like_count(self , obj):
    return CommentLike.objects.filter(comment = obj ).count()
  
  def get_is_comment_liked(self , obj):
    user = self.context.get("request").user
    if user.is_authenticated:
      return CommentLike.objects.filter(user= user, comment = obj).exists()
    return False

  class Meta:
    model = Comment
    fields = ["id" , "user" , "post","commentcontent","comment_like_count" , "is_comment_liked", "created_at"]
  
class CommentLikeSerializer(serializers.ModelSerializer):
  class Meta:
    model = CommentLike
    fields = ["id" , "user" , "comment" , "post" , "created_at"]

  

