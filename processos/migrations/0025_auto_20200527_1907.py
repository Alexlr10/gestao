# Generated by Django 2.0 on 2020-05-27 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0024_auto_20200527_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='Foto',
            field=models.ImageField(default=0, upload_to='profile', verbose_name='Foto'),
            preserve_default=False,
        ),
    ]
