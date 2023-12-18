from django.urls import path
from . import views

urlpatterns = [
    path('' , views.wall),
    path('crearMensaje/<int:id>', views.crearMensaje),
    path('crearComentario/<int:id>', views.crearComentario),
    path('delete/<int:id>' , views.delete),
    path('muro_jugador/' , views.muro_jugador , name='muro_usuario'),
    path('agregar_amigo/<int:amigo_id>/', views.agregar_amigo, name='agregar_amigo'),
    path('lista_amigos/', views.lista_amigos, name='lista_amigos'),

]