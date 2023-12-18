from datetime import timezone
from django.db import models
from login.models import User

class Mensaje(models.Model):
    usuario = models.ForeignKey(User, related_name='mensajes', on_delete= models.CASCADE)
    mensaje = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def puede_eliminar(self):
        tiempo_transcurrido = timezone.now() - self.created_at
        return tiempo_transcurrido.total_seconds() <= 1800  # 1800 segundos = 30 minutos

    def __repr__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\n'
    def __str__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\n'

class Comentario(models.Model):
    usuario = models.ForeignKey(User, related_name='comentarios_user', on_delete= models.CASCADE)
    mensaje = models.ForeignKey(Mensaje, related_name='comentarios_mensaje', on_delete= models.CASCADE)
    comentario = models.TextField(default='Mensaje Vacio')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\nComentario: {self.comentario}'
    def __str__(self):
        return f'Usuario: {self.usuario}\nMensaje: {self.mensaje}\nComentario: {self.comentario}'
