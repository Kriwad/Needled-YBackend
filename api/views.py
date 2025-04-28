
from .serializer import UserSerializer , ToDoSerializer ,DetailUserSerializer , CommentSerializer , LikeSerializer
from .models import CustomUser , ToDoList , Comment , Like , ToDoVideo , ToDoImage
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
class CreateToDoListView(generics.CreateAPIView):

  queryset = ToDoList.objects.all()
  serializer_class= ToDoSerializer
  permission_classes = [IsAuthenticated]

  def create(self, request, *args, **kwargs):
    title = request.data.get('title')
    goal = request.data.get('goal')
    has_images = 'image' in request.FILES
    has_videos =  'video' in request.FILES

    if not (title or goal or has_images or has_videos):
      return Response({"error": "You must provide at least one of: title, goal, image, or video"}, 
                         status=status.HTTP_400_BAD_REQUEST)
    todo = ToDoList.objects.create(
      user = request.user,
      title = title, 
      goal = goal,
      
    )
    images = request.FILES.getlist('image')
    for image in images:
      ToDoImage.objects.create(todo = todo , image= image)
    
    videos = request.FILES.getlist('video')
    for video in videos:
      ToDoVideo.objects.create(todo = todo , video = video)

    serializer = self.get_serializer(todo)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

#lists all todo for home page
class ListTodoView(generics.ListAPIView):
  serializer_class = ToDoSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
   return ToDoList.objects.all().order_by("-created_at")
  
# lists the clicked todo for the comment page
class ListToDoDetailView(generics.RetrieveAPIView):
  serializer_class = ToDoSerializer
  permission_classes = [IsAuthenticated]
  


  def get_queryset(self):
    todo_id = self.kwargs["pk"]
    return ToDoList.objects.filter(id = todo_id)
# helps in editing and updating todos



class EditToDoListView(generics.RetrieveUpdateDestroyAPIView):
 
  serializer_class = ToDoSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):   
    return ToDoList.objects.filter(user = self.request.user )
  
  def update(self , request , *args , **kwargs):
    todo = self.get_object()

    todo.title = request.data.get("title",todo.title)
    todo.goal = request.data.get("goal", todo.goal)
    todo.save()

    images = request.FILES.getlist('image')
    if images:
        for image in images:
          ToDoImage.objects.create(todo=todo, image=image)
        
        # Handle videos update
    videos = request.FILES.getlist('video')
    if videos:
      for video in videos:
        ToDoVideo.objects.create(todo=todo, video=video)
        
    serializer = self.get_serializer(todo)
    return Response(serializer.data)



#fetches and edit the clicked user
class DetailUserView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = DetailUserSerializer
  permission_classes = [IsAuthenticated]
  lookup_field = "id"

  def get_queryset(self):
    user_id = self.kwargs["id"]
    return CustomUser.objects.filter(id = user_id)
  


# lists the users profile todos
class ListUserToDoView(generics.ListAPIView):
 
  serializer_class = ToDoSerializer
  permission_classes = [IsAuthenticated]
 

  def get_queryset(self):   
    user_id = self.kwargs["user_id"]
    return ToDoList.objects.filter(user_id = user_id ).order_by("-created_at")


#Like and Comment 
class ToggleLikeView(generics.ListCreateAPIView):
  serializer_class = LikeSerializer
  permission_classes = [AllowAny]
  lookup_kwarg_field = "todo_id"
  
  def get_queryset(self):
    todo_id = self.kwargs.get("todo_id")
    return Like.objects.filter(todo_id= todo_id).select_related('user')

  def post(self , request , *args , **kwargs):
    todo_id = self.kwargs.get("todo_id")
    todo = ToDoList.objects.get(id = todo_id)
    user = request.user

    like = Like.objects.filter(user = user , todo = todo).first()
    
    if like:
      like.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
    else:
      like = Like.objects.create(user = user , todo= todo)
      serializer = self.get_serializer(like)
      return Response(serializer.data, status=status.HTTP_201_CREATED)



