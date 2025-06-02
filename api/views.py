
from .serializer import UserSerializer , PostsSerializer ,DetailUserSerializer , CommentSerializer , LikeSerializer
from .models import CustomUser , PostsList , Comment , Like , PostsVideo , PostsImage , CommentLike
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser 
from rest_framework import generics , viewsets
from rest_framework.response import Response 
from rest_framework import status
import traceback
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view , permission_classes
from django.views.decorators.csrf import csrf_exempt
#creates user
class CreateUserView(generics.CreateAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

# only admin
class ListUserView(generics.ListAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = UserSerializer
  permission_classes= [IsAdminUser]

# only admin
class ListActiveUserView(generics.ListAPIView):
  queryset = CustomUser.objects.filter(is_active= True)
  serializer_class = UserSerializer
  permission_classes= [IsAdminUser]

  
#fetches current logged in user
class CurrentUserView(generics.RetrieveAPIView):
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated]

  def get_object(self):
    return self.request.user
  
# only authenticated and current user
class CreatePostsListView(generics.CreateAPIView):

  queryset = PostsList.objects.all()
  serializer_class= PostsSerializer
  permission_classes = [IsAuthenticated]

  def create(self, request, *args, **kwargs):
    title = request.data.get('title')
    content = request.data.get('content')
    has_images = 'image' in request.FILES
    has_videos =  'video' in request.FILES
    
    if not (title or content or has_images or has_videos):
      return Response({"error": "You must provide at least one of: title, content, image, or video"}, 
                         status=status.HTTP_400_BAD_REQUEST)
    post = PostsList.objects.create(
      user = request.user,
      title = title, 
      content = content,
      
    )
    images = request.FILES.getlist('image')
    for image in images:
      PostsImage.objects.create(post = post , image= image)
    
    videos = request.FILES.getlist('video')
    for video in videos:
      PostsVideo.objects.create(post = post , video = video)

    serializer = self.get_serializer(post)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

#lists all post for home page
class ListPostsView(generics.ListAPIView):
  serializer_class = PostsSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
   return PostsList.objects.all().order_by("-created_at")
  
# lists the clicked post for the comment page
class ListPostsDetailView(generics.RetrieveAPIView):
  serializer_class = PostsSerializer
  permission_classes = [IsAuthenticated]
  


  def get_queryset(self):
    post_id = self.kwargs["pk"]
    return PostsList.objects.filter(id = post_id)
# helps in editing and updating posts



class EditPostsListView(generics.RetrieveUpdateDestroyAPIView):
 
  serializer_class = PostsSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):   
    return PostsList.objects.filter(user = self.request.user )
  
  def update(self , request , *args , **kwargs):
    post = self.get_object()

    post.title = request.data.get("title",post.title)
    post.content = request.data.get("content", post.content)
    post.save()

    images = request.FILES.getlist('image')
    if images:
        for image in images:
          PostsImage.objects.create(post=post, image=image)
        
        # Handle videos update
    videos = request.FILES.getlist('video')
    if videos:
      for video in videos:
        PostsVideo.objects.create(post=post, video=video)
        
    serializer = self.get_serializer(post)
    return Response(serializer.data)



#fetches and edit the clicked user
class DetailUserView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = DetailUserSerializer
  permission_classes = [IsAuthenticated]
  lookup_field = "id"

  queryset = CustomUser.objects.all()
  


# lists the users profile posts
class ListUserPostsView(generics.ListAPIView):
 
  serializer_class = PostsSerializer
  permission_classes = [IsAuthenticated]
 

  def get_queryset(self):   
    user_id = self.kwargs["user_id"]
    return PostsList.objects.filter(user_id = user_id ).order_by("-created_at")


#Like and Comment 
class ToggleLikeView(generics.ListCreateAPIView):
  serializer_class = LikeSerializer
  permission_classes = [IsAuthenticated]

  
  def get_queryset(self):
    post_id = self.kwargs.get("post_id")
    return Like.objects.filter(post_id= post_id).select_related('user')

  def post(self , request , *args , **kwargs):
    post_id = self.kwargs.get("post_id")
    post = PostsList.objects.get(id = post_id)
    user = request.user

    like = Like.objects.filter(user = user , post = post).first()
    
    if like:
      like.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    else:
      like = Like.objects.create(user = user , post= post)
      serializer = self.get_serializer(like)
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST" , "GET"])
@permission_classes([IsAuthenticated])

def CreateCommentView(request , post_id):

  try:
    post = PostsList.objects.get(id = post_id)
  except PostsList.DoesNotExist:
    return Response({"error":"THe post doesnot exist"})
  
  if request.method == "POST":
    try:      
      commentcontent = request.data.get("commentcontent")

      if not commentcontent:
        return Response({"error": "comment content are required."}, status=400)

      try:
        post = PostsList.objects.get(id = post_id)
      except PostsList.DoesNotExist:
          return Response({"error": "Post doesnot exists"} , status = 404)

      
      comment =Comment.objects.create(user = request.user ,post = post,  commentcontent = commentcontent )
      serializer = CommentSerializer(comment , context = {'request': request})
      return Response(serializer.data, status = 201)
    except Exception as e:
   
      print("\n--- ERROR IN CREATECOMMENTVIEW ---")
      traceback.print_exc() 
      print("--- END ERROR IN CREATECOMMENTVIEW ---\n")
      
      return Response({"error": "something went wrong" , "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  elif request.method == "GET":
       
    comments = Comment.objects.filter(post= post).select_related("user")
    serialized = CommentSerializer(comments , context = {'request': request},many = True)
    return Response(serialized.data  , status = 200)
  
@api_view([ "PATCH" , "DELETE"])
@permission_classes([IsAuthenticated])
def UpdateDeleteCommentView(request , comment_id):
 
    
    try:
      comment = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist:
      return Response({"error": "Coment Doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    
    if comment.user != request.user:
      return Response({"error": "You dont have permission to edit this comment "} , status=status.HTTP_403_FORBIDDEN)
    if request.method == "PATCH":
      serializer = CommentSerializer(comment , data=request.data , partial = True , context = { 'request': request})

      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":

      try:
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
      except Comment.DoesNotExist :
        return Response({"error": "Comment Doesnot exist"}, status = status.HTTP_404_NOT_FOUND)
      except Exception as e:
        print("\n---ERROR IN DELETE CommentView")
        traceback.print_exc()
        print("\n--END ERROR IN DELETE Comment View----\n")
        return Response({"error": "Something went wrong during deletion"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ToggleCommentLikeView(request,comment_id):
  try:
    comment = Comment.objects.get(id = comment_id )
  except Comment.DoesNotExist:
    return Response({"error": 'This comment doesnot exist'})

  comment_like = CommentLike.objects.filter(user = request.user, comment = comment).first()

  if comment_like:
    comment_like.delete()
    return Response("Like deleted" , status= 201)
  else:
    new_comment_like = CommentLike.objects.create(user = request.user , comment = comment)
    return Response({"id": new_comment_like.id} , status = 201)

