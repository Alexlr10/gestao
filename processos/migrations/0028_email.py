# Generated by Django 2.0 on 2020-05-29 15:50

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0027_auto_20200528_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('presenca', models.ManyToManyField(blank=True, null=True, related_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]