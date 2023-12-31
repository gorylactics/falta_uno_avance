from django.urls import path
from . import views


urlpatterns = [
    path('' , views.index , name="index"),
    path('registrar/', views.registrar),
    path('login/', views.login),
    path('success/', views.success),
    path('logout/', views.logout),
    path('editar/<int:id>', views.editar),
    path('usuarios/' , views.muestra_usuarios_api, name='usuarios'),
]
