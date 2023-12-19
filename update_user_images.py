# update_user_images.py
import os
from django.core.wsgi import get_wsgi_application
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'muro.settings')
application = get_wsgi_application()

from login.models import User
from django.conf import settings

def update_user_images():
    users_without_image = User.objects.filter(imagen__isnull=True)

    default_image_path = 'img/avatar_usuario.jpeg'

    for user in users_without_image:
        # Construir la ruta completa al archivo de la imagen por defecto
        default_image_full_path = os.path.join(settings.BASE_DIR, default_image_path)

        # Abrir el archivo y asignarlo al campo de la imagen del usuario
        with open(default_image_full_path, 'rb') as f:
            user.imagen.save(os.path.basename(default_image_full_path), File(f), save=True)

if __name__ == '__main__':
    update_user_images()

