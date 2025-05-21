
from .serializer import UserSerializer , PostsSerializer ,DetailUserSerializer , CommentSerializer , LikeSerializer
from .models import CustomUser , PostsList , Comment , Like , PostsVideo , PostsImage
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser 
from rest_framework import generics , viewsets
from rest_framework.response import Response
from rest_framework import status

#creates user
class CreateUserView(generics.CreateAPIView):
  queryset = CustomUser.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

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

  def get_queryset(self):
    user_id = self.kwargs["id"]
    return CustomUser.objects.filter(id = user_id)
  


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
  permission_classes = [AllowAny]
  lookup_kwarg_field = "post_id"
  
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



