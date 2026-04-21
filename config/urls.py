from django.urls import path, include
from vehicles.admin_site import custom_admin_site

urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('', include('vehicles.urls')),
]