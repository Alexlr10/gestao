# Generated by Django 2.0 on 2020-05-28 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0025_auto_20200527_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='Foto',
            field=models.ImageField(blank=True, null=True, upload_to='profile', verbose_name='Foto'),
        ),
    ]
