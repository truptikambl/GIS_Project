from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('maps.urls')),  # Use this instead of 'maps.api_urls'
    path('', include('maps.urls')),      # This enables root URL or 'map/' to work
]
