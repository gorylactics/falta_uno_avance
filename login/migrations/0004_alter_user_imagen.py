# Generated by Django 4.2.6 on 2023-12-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_remove_user_date_birth_user_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imagen',
            field=models.ImageField(blank=True, default='img/avatar_usuario.jpeg', help_text='Imagen perfil', null=True, upload_to='foto_perfil', verbose_name='Imagen Perfil'),
        ),
    ]
