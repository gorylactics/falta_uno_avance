from django.shortcuts import render , redirect
from .models import *
# from ..login.models import *
from django.contrib import messages
from datetime import datetime, time, timedelta
from django.utils import timezone
from login.models import User


def wall(request):
    if 'usuario' not in request.session:
        return redirect('/')
    else:
        usuario = User.objects.get(id=request.session['usuario']['id'])
        mensajes = Mensaje.objects.all().order_by('-created_at')
        cantMensajes = len(mensajes)
        comentarios = Comentario.objects.all()
        cantComentarios = len(comentarios)
        usuarios = User.objects.exclude(id=request.session['usuario']['id'])  
        # Excluir al propio usuario de la lista de amigos sugeridos
        contexto = {
            'usuario': usuario,
            'mensajes': mensajes,
            'comentarios': comentarios,
            'usuarios': usuarios,
            'cantMensajes': cantMensajes,
            'cantComentarios': cantComentarios,
        }
        return render(request, 'wall.html', contexto)

def agregar_amigo(request, amigo_id):
    if 'usuario' in request.session:
        usuario_actual = request.session['usuario']
        usuario_id = usuario_actual['id']
        usuario = User.objects.get(id=usuario_id)
        amigo = User.objects.get(id=amigo_id)

        usuario.amigos.add(amigo)
        usuario.save()

        messages.success(request, f'Ahora eres amigo de {amigo.first_name} {amigo.last_name}!')

        return redirect('/wall')
    else:
        return redirect('/')

def lista_amigos(request):
    if 'usuario' in request.session:
        usuario_actual = request.session['usuario']
        usuario_id = usuario_actual['id']
        usuario = User.objects.get(id=usuario_id)
        amigos = usuario.amigos.all()

        contexto = {
            'titulo': 'Lista de Amigos',
            'request': request,
            'amigos': amigos,
        }

        return render(request, 'lista_amigos.html', contexto)
    else:
        return redirect('/')

def crearMensaje(request , id):
    usuario = User.objects.get(id = id)
    mensaje = Mensaje.objects.create(
        usuario = usuario,
        mensaje = request.POST['mensaje'],
    )
    return redirect('/wall')


def mensajes_amigo(request, amigo_id):
    amigo = get_object_or_404(User, id=amigo_id)
    mensajes = Mensaje.objects.filter(usuario=amigo).order_by('-created_at')
    
    contexto = {
        'amigo': amigo,
        'mensajes': mensajes,
    }

    return render(request, 'mensajes_amigo.html', contexto)


def crearComentario(request, id):
    mensaje = Mensaje.objects.get(id = id)
    usuario_comentador = User.objects.get(id = request.session['usuario']['id'])
    comentario = Comentario.objects.create(
        mensaje = mensaje,
        comentario = request.POST['comentario'],
        usuario = usuario_comentador,
    )
    return redirect('/wall')

def minutos(fecha):
    today = timezone.now()
    resultado = (today.year - fecha.year)*365*24*60 + (today.month - fecha.month)*30*24*60 + (today.day - fecha.day)*24*60 + (today.hour-fecha.hour)*60 + (today.minute-fecha.minute)
    return resultado

def delete(request , id):
    usuario = User.objects.get(id = request.session['usuario']['id'])
    mensaje = Mensaje.objects.get(id = id)

    calcular_tiempo = minutos(mensaje.created_at)
    if calcular_tiempo > 30:
        messages.warning(request, "Han pasado mas de 30 min, no puedes borrar el mensaje")
        return redirect('/wall')
    else: 
        messages.success(request ,'Borrado con exito')
        mensaje.delete()
        return redirect("/wall")


def muro_jugador(request):
    usuario_actual = request.session.get('usuario')
    if usuario_actual:
        usuario_id = usuario_actual['id']
        print(usuario_actual)
        print(usuario_id)
        mensajes = Mensaje.objects.filter(usuario = usuario_id).order_by('-created_at')
        cantMensajes = mensajes.count()
        contexto = {
            'titulo': 'Perfil de Usuario',
            'request': request,
            'cantMensajes': cantMensajes,
            'mensajes': mensajes,
        }
        return render(request, '/muro_jugador', contexto)
    else:
        return redirect('/')


from django.shortcuts import render, get_object_or_404
from django.contrib import messages
# from .models import User  # Asegúrate de importar tu modelo de usuario

def perfil_amigo(request, amigo_id):
    amigo = get_object_or_404(User, id=amigo_id)
    mensajes = Mensaje.objects.filter(usuario=amigo).order_by('-created_at')

    # Imprimir mensajes para verificar
    for mensaje in mensajes:
        print(mensaje.mensaje)

    contexto = {
        'amigo': amigo,
        'mensajes': mensajes,
    }

    return render(request, 'perfil_amigo.html', contexto)


def eliminar_amigo(request, amigo_id):
    if 'usuario' in request.session:
        usuario_actual = request.session['usuario']
        usuario_id = usuario_actual['id']
        
        usuario = get_object_or_404(User, id=usuario_id)
        amigo = get_object_or_404(User, id=amigo_id)

        # Eliminar al amigo
        usuario.amigos.remove(amigo)
        usuario.save()

        messages.success(request, f'Has eliminado a {amigo.first_name} {amigo.last_name} de tu lista de amigos.')

    return redirect('lista_amigos')