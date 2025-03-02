
from .serializer import UserSerializer , ToDoSerializer ,DetailUserSerializer , CommentSerializer , LikeSerializer
from .models import CustomUser , ToDoList , Comment , Like
from rest_framework.permissions import AllowAny , IsAuthenticated , IsAdminUser 
from rest_framework import generics , viewsets

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

  def perform_create(self, serializer):
    
    serializer.save(user= self.request.user)

#lists all todo for home page
class ListTodoView(generics.ListAPIView):
  serializer_class = ToDoSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
   return ToDoList.objects.all().order_by("-created_at")

# helps in editing and updating todos



class EditToDoListView(generics.RetrieveUpdateDestroyAPIView):
 
  serializer_class = ToDoSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):   
    return ToDoList.objects.filter(user = self.request.user )

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

