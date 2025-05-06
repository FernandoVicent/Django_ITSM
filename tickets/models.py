from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    CATEGORIAS = [
        ('Rede', 'Rede'),
        ('Infraestrutura', 'Infraestrutura'),
        ('Software', 'Software'),
    ]
    PRIORIDADES = [
        ('Baixa', 'Baixa'),
        ('Média', 'Média'),
        ('Alta', 'Alta'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    prioridade = models.CharField(max_length=20, choices=PRIORIDADES)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pendente')  # pode ser alterado depois

    def __str__(self):
        return f"Case{self.id} - {self.titulo}"
