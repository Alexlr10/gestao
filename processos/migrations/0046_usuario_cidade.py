# Generated by Django 3.0.7 on 2021-01-21 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processos', '0045_auto_20210121_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cidade',
            field=models.CharField(default=1, max_length=10, verbose_name='Cidade'),
            preserve_default=False,
        ),
    ]
