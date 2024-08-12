from django.urls import path, include
from django.contrib import admin
from LittleLemonAPI.views import UserDeleteView  # Correct import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('LittleLemonAPI.urls')),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),  # If using JWT for authentication
    path('api/auth/', include('djoser.urls.authtoken')),  # If using token-based auth
     path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),
]