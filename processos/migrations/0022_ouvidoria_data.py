# Generated by Django 2.0 on 2020-05-09 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0021_ouvidoria'),
    ]

    operations = [
        migrations.AddField(
            model_name='ouvidoria',
            name='data',
            field=models.DateField(blank=True, null=True, verbose_name='data'),
        ),
    ]
