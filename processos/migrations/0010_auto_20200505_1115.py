# Generated by Django 2.0 on 2020-05-05 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0009_servico_descricao'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reuniao',
            name='ausencia',
        ),
        migrations.RemoveField(
            model_name='reuniao',
            name='presenca',
        ),
    ]
