from django.contrib import admin
from .models import User 
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name' , 'email' , 'password')
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
admin.site.register(User , UserAdmin)
