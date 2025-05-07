from django.db import models
from django.contrib.auth.models import User

# class Ticket(models.Model):
#     CATEGORIAS = [
#         ('Rede', 'Rede'),
#         ('Infraestrutura', 'Infraestrutura'),
#         ('Software', 'Software'),
#     ]
#
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     titulo = models.CharField(max_length=200)
#     descricao = models.TextField()
#     categoria = models.CharField(max_length=50, choices=CATEGORIAS)
#     criado_em = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, default='Aberto')
#     descricao_tecnico = models.TextField(blank=True)# pode ser alterado depois
#
#     def __str__(self):
#         return f"Case{self.id} - {self.titulo}"
# models.py
from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    STATUS_CHOICES = [
        ("Aberto", "Aberto"),
        ("Em andamento", "Em andamento"),
        ("Resolvido", "Resolvido"),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    usuario = models.ForeignKey(User, related_name='chamados', on_delete=models.CASCADE)
    tecnico_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chamados_designados')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Aberto")
    criado_em = models.DateTimeField(auto_now_add=True)
    descricao_tecnico = models.TextField(blank=True)

    def __str__(self):
        return f"TKT-{self.id:04d}"

class LogChamado(models.Model):
    chamado = models.ForeignKey(Ticket, related_name='logs', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    acao = models.TextField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.chamado.id} - {self.usuario.username} em {self.data}"
