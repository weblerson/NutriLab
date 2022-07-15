from django.urls import path
from . import views
from .api import api

urlpatterns = [
    # Dados Paciente
    path('pacientes/', views.pacientes, name = 'pacientes'),
    path('pacientes/dados', views.dados_paciente, name = 'dados_paciente'),
    path('pacientes/dados/<str:id>', views.dados, name = 'dados'),
    path('pacientes/dados/grafico/<str:id>/', views.grafico, name = 'grafico'),

    # Plano Alimentar
    path('pacientes/plano_alimentar', views.lista_plano_alimentar, name='lista_plano_alimentar'),
    path('pacientes/plano_alimentar/<str:id>', views.plano_alimentar, name='plano_alimentar'),
    path('refeicao/<str:id>', views.refeicao, name='refeicao'),
    path('opcao/<str:id>', views.opcao, name='opcao'),

    # HTML - PDF
    path('', api.urls)
]