from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('mock_app.urls')),
    path('api/admin/', include('auth_system.urls')),
]
