from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('wms/', include('warehouse.urls')),
    path('', include('guessgame_app.urls')),
]