# Generated by Django 4.0.6 on 2022-07-08 14:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plataforma', '0003_dadospaciente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refeicao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('horario', models.TimeField()),
                ('carboidratos', models.IntegerField()),
                ('proteinas', models.IntegerField()),
                ('gorduras', models.IntegerField()),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Opcao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagem', models.ImageField(upload_to='opcao')),
                ('descricao', models.TextField()),
                ('refeicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.refeicao')),
            ],
        ),
    ]
