# Generated by Django 2.0 on 2020-05-22 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0004_balanco_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='despesas',
            name='Pagamento',
            field=models.BooleanField(default=True, verbose_name='Pagamento Efetuado'),
        ),
    ]