# Generated by Django 2.0 on 2020-05-29 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0028_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='email',
            old_name='presenca',
            new_name='membro',
        ),
    ]