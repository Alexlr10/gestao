# Generated by Django 2.0 on 2020-05-27 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0018_auto_20200527_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ata',
            name='Arquivo',
            field=models.FileField(default='', upload_to='Files', verbose_name='Arquivo'),
        ),
    ]
