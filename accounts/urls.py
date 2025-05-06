from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    # path('usuario/dashboard/', views.dashboard_usuario, name='dashboard_usuario'),

]
