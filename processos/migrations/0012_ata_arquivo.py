# Generated by Django 2.0 on 2020-05-27 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0011_auto_20200526_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='ata',
            name='Arquivo',
            field=models.FileField(default=0, upload_to='', verbose_name='Arquivo'),
            preserve_default=False,
        ),
    ]