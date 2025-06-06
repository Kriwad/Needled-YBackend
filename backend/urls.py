
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path , include
from rest_framework_simplejwt.views import TokenObtainPairView , TokenRefreshView





urlpatterns = [
   
    path('admin/', admin.site.urls),
    path('api/token/refresh/' , TokenRefreshView.as_view() , name = 'refresh' ),
    path('api/token/' , TokenObtainPairView.as_view() , name = 'get_token' ),

    path('api/' , include('api.urls') ),
    
    path('api-auth/' , include('rest_framework.urls')),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)