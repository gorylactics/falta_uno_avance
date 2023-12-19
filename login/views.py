from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# import re

def index(request):
    if request.method  == 'GET':
        contexto = {'titulo' : 'Login/Registro'}
        return render(request , 'index.html' , contexto)

def registrar(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            for key, value in errores.items():
                messages.warning(request, value)
            # Resto del código para manejar errores
        else:
            encriptacion = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=encriptacion,
            )
            imagen = request.FILES.get('imagen')
            if imagen:
                # Si el usuario proporciona una imagen, la guardamos
                user.imagen = imagen
                user.save()
            else:
                # Si no hay imagen proporcionada, asignamos la imagen predeterminada
                default_image_path = 'img/avatar_usuario.jpeg'
                default_image_content = default_storage.open(default_image_path).read()
                content_file = ContentFile(default_image_content)
                user.imagen.save('avatar_usuario.jpeg', content_file)
                user.save()

            # Establecer la información del usuario en la sesión
            sesion_de_usuario = {
                'id': user.id,
                'nombre': user.first_name,
                'apellido': user.last_name,
                'email': user.email,
                'created_at': user.created_at.strftime('%Y-%m-%d'),
                'imagen_url': user.imagen.url if user.imagen else None,
            }
            request.session['usuario'] = sesion_de_usuario

            messages.success(request, 'Usuario registrado')
            # Limpiar datos de sesión
            request.session['user_first_name'] = ''
            request.session['user_last_name'] = ''
            request.session['user_email'] = ''
            request.session['user_password'] = ''
            request.session['user_password_confirm'] = ''
            return redirect('/success/')



def login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            user_logeado = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), user_logeado.password.encode()):
                sesion_de_usuario = {
                    'id': user_logeado.id,
                    'nombre': user_logeado.first_name,
                    'apellido': user_logeado.last_name,
                    'email': user_logeado.email,
                    'created_at': user_logeado.created_at.strftime('%Y-%m-%d'),
                    'imagen_url': user_logeado.imagen.url if user_logeado.imagen else None,
                }
                request.session['usuario'] = sesion_de_usuario
                request.session['user_email_login'] = ''
                request.session['user_password_login'] = ''

                # Limpiar la URL de la imagen anterior si existe
                if 'usuario_imagen_url' in request.session:
                    del request.session['usuario_imagen_url']

                # Actualizar la URL de la imagen en la sesión si ha cambiado
                if 'usuario' in request.session and 'imagen_url' in request.session['usuario']:
                    request.session['usuario']['imagen_url'] = user_logeado.imagen.url if user_logeado.imagen else None

                return redirect('/success/')
            else:
                messages.warning(request, 'Contraseña incorrecta. Inténtelo de nuevo.')
                request.session['user_email_login'] = request.POST['email']
                request.session['user_password_login'] = request.POST['password']
                return redirect('/')
        else:
            messages.warning(request, 'Correo electrónico no válido. Inténtelo de nuevo.')
            request.session['user_email_login'] = request.POST['email']
            request.session['user_password_login'] = request.POST['password']
            return redirect('/')


def success(request):
    if 'usuario' in request.session:
        contexto = {'titulo': 'Exito',}
        # return render(request , 'success.html' ,contexto)
        print('accediendo desde el metodo GET', request.GET)
        return redirect('/wall/')
    else:
        return redirect('/')

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
        # Verificar si la clave está presente antes de intentar eliminarla
        if 'usuario_imagen_url' in request.session:
            del request.session['usuario_imagen_url']
    return redirect('/')


def editar(request, id):
    # Verificar si el usuario está autenticado
    if 'usuario' not in request.session:
        return redirect('/')

    usuario_logueado_id = request.session['usuario']['id']

    # Verificar si el usuario tiene permisos para editar el perfil
    if request.method == 'GET':
        # Obtener el usuario a editar
        usuario = User.objects.get(id=id)

        # Verificar si el usuario logueado tiene permisos para editar este perfil
        if usuario.id != usuario_logueado_id:
            messages.warning(request, 'No tienes permisos para editar este perfil.')
            return redirect('/wall')

        contexto = {
            'titulo': 'Editar',
            'usuario': usuario,  # Pasar el objeto usuario al contexto
        }
        return render(request, 'editar.html', contexto)
    
    if request.method == 'POST':
        # Obtener el usuario a editar
        usuario = User.objects.get(id=id)
        
        # Verificar si el usuario logueado tiene permisos para editar este perfil
        if usuario.id != usuario_logueado_id:
            messages.warning(request, 'No tienes permisos para editar este perfil.')
            return redirect('/wall')

        # Validar datos del formulario
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            for key, value in errores.items():
                messages.warning(request, value)
            
            return redirect('/editar/' + str(id))  # Redirigir de nuevo al formulario de edición
        
        # Actualizar datos del usuario
        usuario.first_name = request.POST['first_name']
        usuario.last_name = request.POST['last_name']
        usuario.email = request.POST['email']

        # Actualizar la contraseña si se proporcionó una nueva
        if request.POST.get('password'):
            encriptacion = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
            usuario.password = encriptacion

        # Actualizar la imagen si se proporcionó una nueva
        imagen_nueva = request.FILES.get('imagen')
        if imagen_nueva:
            # Eliminar la imagen antigua si existe
            if usuario.imagen:
                default_storage.delete(usuario.imagen.name)

            # Guardar la nueva imagen
            usuario.imagen = imagen_nueva

        usuario.save()

        # Actualizar la sesión con los nuevos datos
        sesion_de_usuario = {
            'id': usuario.id,
            'nombre': usuario.first_name,
            'apellido': usuario.last_name,
            'email': usuario.email,
            'created_at': usuario.created_at.strftime('%Y-%m-%d'),
            'imagen_url': usuario.imagen.url if usuario.imagen else None,
        }
        request.session['usuario'] = sesion_de_usuario

        messages.success(request, 'Usuario actualizado exitosamente.')
        print(f'Ruta de la imagen actualizada por el usuario (id={usuario.id}): {usuario.imagen.url if usuario.imagen else None}')
        return redirect('/wall')