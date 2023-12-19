from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),
    path('wall/', include('wall.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
# con la importacion de la linea 3 y 4 mas este if, se garantiza que las imagenes se guarden y muestren en modo debug 