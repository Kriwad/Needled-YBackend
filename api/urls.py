from django.urls import path

from .views import CreatePostsListView ,CreateCommentView  ,UpdateDeleteCommentView, CreateUserView  ,  ListUserPostsView , ListPostsView , ListActiveUserView , ListPostsDetailView , EditPostsListView  , ToggleLikeView ,ToggleCommentLikeView, DetailUserView, CurrentUserView , ListUserView



urlpatterns = [
    path('user/register/', CreateUserView.as_view(), name='register'),
    path('user/all/', ListUserView.as_view(), name='all_user'),
    path('user/active/', ListActiveUserView.as_view(), name='active_user'),
    path("user/current/", CurrentUserView.as_view(), name="currentuser"),
    path('user/post/', CreatePostsListView.as_view(), name='create_post'),
    path('user/post/list/', ListPostsView.as_view(), name='create_post'),
    path('user/list/post/comment/<int:pk>/', ListPostsDetailView.as_view(), name='comments_Posts'),
    path('user/post/edit/<int:pk>/', EditPostsListView.as_view(), name='edit_posts'),
    path('user/post/like/<int:post_id>/' , ToggleLikeView.as_view() , name = "toggle_like"),
    path('user/post/comment/<int:post_id>/' , CreateCommentView , name = "create_comment" ),
    path('user/edit/comment/<int:comment_id>/' , UpdateDeleteCommentView , name = "create_comment" ),
    
    path('user/comment/like/<int:comment_id>/' , ToggleCommentLikeView, name = "create_comment" ),
    path('user/profile/<int:id>/', DetailUserView.as_view(), name='users_nameid'),
   
    path('user/profile/posts/<int:user_id>/',ListUserPostsView.as_view(), name='users_posts'),
    
]


