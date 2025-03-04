
# from .models import ToDo
from rest_framework import serializers
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser , ToDoList , Like  , Comment

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = fields = ['id', 'username', 'password', 'email', 'first_name', 'middle_name', 'last_name', 'fullname', 'image' ]
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

class ToDoSerializer(serializers.ModelSerializer):
  user = DetailUserSerializer( read_only = True)
  like_count = serializers.SerializerMethodField()
  is_liked = serializers.SerializerMethodField()
  class Meta:
    model= ToDoList
    fields = ['user' ,'id', 'title' , 'goal' , 'image', 'video', 'created_at' , 'like_count' , 'is_liked']
    read_only_fields = ['user']
  
  def get_like_count(self , obj):
    return Like.objects.filter(todo = obj).count()
  
  def get_is_liked(self , obj):
    user = self.context.get("request").user
    if user.is_authenticated:
      return Like.objects.filter(user = user , todo= obj).exists() 
    return False

#like and comment

class LikeSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only = True)
  class Meta:
    model = Like
    fields = ["id" , "user" , "created_at"]

class CommentSerializer(serializers.Serializer):
  user = UserSerializer(read_only  = True)
  class Meta:
    model = Comment
    fields = ["id" , "user" , "content", "created_at"]


