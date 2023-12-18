from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt
# import re


def index(request):
    if request.method  == 'GET':
        contexto = {'titulo' : 'Login/Registro'}
        return render(request , 'index.html' , contexto)

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def registrar(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method == 'POST':
        errores = User.objects.validacion(request.POST)
        if len(errores) > 0:
            for key, value in errores.items():
                messages.warning(request, value)
            request.session['user_first_name'] = request.POST['first_name']
            request.session['user_last_name'] = request.POST['last_name']
            request.session['user_email'] = request.POST['email']
            request.session['user_password'] = request.POST['password']
            request.session['user_password_confirm'] = request.POST['password_confirm']
            return redirect('/')
        else:
            encriptacion = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=encriptacion,
            )
            imagen = request.FILES.get('imagen')
            if imagen:
                user.imagen = imagen
                user.save()
                request.session['usuario_imagen_url'] = user.imagen.url
                request.session['usuario'] = {
                    'id': user.id,
                    'nombre': user.first_name,
                    'apellido': user.last_name,
                    'email': user.email,
                    'created_at': user.created_at.strftime('%Y-%m-%d'),
                    'imagen_url': user.imagen.url,
                }
            else:
                # Si no hay imagen, asignar los datos del usuario a la sesión sin la URL de la imagen
                request.session['usuario'] = {
                    'id': user.id,
                    'nombre': user.first_name,
                    'apellido': user.last_name,
                    'email': user.email,
                    'created_at': user.created_at.strftime('%Y-%m-%d'),
                }
            messages.success(request, 'Usuario registrado')
            # Limpiar datos de sesión
            request.session['user_first_name'] = ''
            request.session['user_last_name'] = ''
            request.session['user_email'] = ''
            request.session['user_password'] = ''
            request.session['user_password_confirm'] = ''
            print(request.session['usuario'])
            return redirect('/success/')


def login(request):
    if request.method == 'GET':
        return redirect('/')
    if request.method  == 'POST':
        user = User.objects.filter(email = request.POST['email'])
        if user:
            user_logeado = user[0]
            if bcrypt.checkpw(request.POST['password'].encode() , user_logeado.password.encode()):
                sesion_de_usuario = {
                    'id'         : user_logeado.id,
                    'nombre'     : user_logeado.first_name,
                    'apellido'   : user_logeado.last_name,
                    'email'      : user_logeado.email,
                    'created_at' : user_logeado.created_at.strftime('%Y-%m-%d'),
                    
                    # aca no se puede guardar un objeto completo , hay que separarlo por partes para que pueda ser tomado
                }
                request.session['usuario'] = sesion_de_usuario
                print(f'la sesion de usuario es: {user_logeado}' )
                print(f'el post es: {request.POST}')
                request.session['user_email_login'] = ''
                request.session['user_password_login'] = ''
                return redirect('/success/')
            else:
                messages.warning(request ,'Contraseña Invalida')
                request.session['user_email_login'] = request.POST['email']
                request.session['user_password_login'] = request.POST['password']
                return redirect('/')
        else:
            messages.warning(request ,'Correo Invalido')
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
    request.session.clear()
    return redirect('/')

def editar(request , id):
    if 'usuario' in request.session:
        if request.method == 'GET':
            contexto = {'titulo': 'Editar',}
            return render(request ,'editar.html')
        if request.method == 'POST':
            errores = User.objects.validacion(request.POST)
            if len(errores) > 0:
                for key , value in errores.items():
                    messages.warning(request , value)
                request.session['user_first_name'] = request.POST['first_name']
                request.session['user_last_name'] = request.POST['last_name']
                request.session['user_email'] = request.POST['email']
                request.session['user_password'] = request.POST['password']
                request.session['user_password_confirm'] = request.POST['password_confirm']
                return redirect('/wall')
            else:
                usuario = User.objects.get(id = id)
                usuario_logueado = request.session['usuario']['id']
                if usuario.id == usuario_logueado:
                    encriptacion = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
                    usuario.first_name = request.POST['first_name']
                    usuario.last_name = request.POST['last_name']
                    usuario.email = request.POST['email']
                    usuario.password = encriptacion
                    usuario.save()
                    messages.success( request,'Usuario Actualizado')
                    return redirect('/wall')
                else:
                    print('los usuarios son diferentes')
                    return redirect('/')
    else:
        return redirect('/')
        print(f'Desde la vista de editar imprimiendo el metodo GET {request.GET}')
        print(f'Desde la vista de editar imprimiendo el metodo POST {request.POST}')
        return redirect('/wall/')