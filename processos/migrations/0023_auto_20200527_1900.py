# Generated by Django 2.0 on 2020-05-27 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0022_auto_20200527_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ata',
            name='Arquivo',
            field=models.FileField(blank=True, default='', null=True, upload_to='Files', verbose_name='Arquivo'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='Foto',
            field=models.ImageField(upload_to='profile', verbose_name='Foto'),
        ),
    ]
