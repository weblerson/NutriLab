from django.contrib import admin
from .models import Paciente, DadosPaciente, Refeicao, Opcao

# Register your models here.

admin.site.register(Paciente)
admin.site.register(DadosPaciente)
admin.site.register(Refeicao)
admin.site.register(Opcao)