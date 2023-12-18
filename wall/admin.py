from django.contrib import admin
from .models import Comentario , Mensaje ,User
# Register your models here.


class MensajeAdmin(admin.ModelAdmin):
    list_display = ('usuario' , 'mensaje')
    class Meta:
            verbose_name = 'Mensaje'
            verbose_name_plural = 'Mensajes'

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario' , 'mensaje' , 'comentario' )
    class Meta:
            verbose_name = 'Comentario'
            verbose_name_plural = 'Comentarios'

admin.site.register(Mensaje , MensajeAdmin)    
admin.site.register(Comentario , ComentarioAdmin)
