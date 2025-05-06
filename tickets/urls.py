from django.urls import path
from . import views
from .views import criar_chamado

urlpatterns = [
    path('criar/', criar_chamado, name='criar_chamado'),
    path('tecnico/chamados/', views.dashboard_tech, name='painel_tecnico'),
    path('usuario/dashboard/', views.dashboard_usuario, name='dashboard_usuario'),
]
