# Generated by Django 4.0.6 on 2022-07-06 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_recuperacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recuperacao',
            name='ativo',
            field=models.BooleanField(default=False),
        ),
    ]
