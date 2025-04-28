from django.urls import path

from .views import CreateUserView,ListActiveUserView, ListUserView ,ListToDoDetailView, CreateToDoListView , EditToDoListView ,ListTodoView , CurrentUserView ,DetailUserView , ListUserToDoView, ToggleLikeView



urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='register'),
    path('user/all/', ListUserView.as_view(), name='all_user'),
    path('user/active/', ListActiveUserView.as_view(), name='active_user'),
    path("user/current/", CurrentUserView.as_view(), name="currentuser"),
    path('user/todo/', CreateToDoListView.as_view(), name='todo'),
    path('user/todo/list/', ListTodoView.as_view(), name='todo'),
    path('user/list/todo/comment/<int:pk>/', ListToDoDetailView.as_view(), name='comments_todos'),
    path('user/todo/edit/<int:pk>/', EditToDoListView.as_view(), name='edit_todo'),
    path('user/todo/like/<int:todo_id>/' , ToggleLikeView.as_view() , name = "toggle_like"),

    path('user/profile/<int:id>/', DetailUserView.as_view(), name='users_nameid'),
   
    path('user/profile/todos/<int:user_id>/',ListUserToDoView.as_view(), name='users_todo'),
    
]


