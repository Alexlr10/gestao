# Generated by Django 2.0 on 2020-05-26 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0009_auto_20200525_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receita',
            name='parcelado',
        ),
        migrations.AddField(
            model_name='receita',
            name='parcela',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Parcela'),
        ),
    ]
