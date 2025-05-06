from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TicketForm
from .models import Ticket

@login_required
def criar_chamado(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.usuario = request.user
            chamado.save()
            messages.success(request, f'Novo chamado criado: {chamado.titulo}')
            return redirect('dashboard_usuario')  # Redireciona de volta para a página de Meus Chamados
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

@login_required
def dashboard_usuario(request):
    return render(request, 'usuario_dashboard.html')
#

@login_required
def dashboard_tech(request):
    if not request.user.is_staff:
        return redirect('user_dashboard')  # Protege contra acesso indevido

    tickets = Ticket.objects.all().order_by('-criado_em')  # Ajuste o campo se necessário

    # Contadores por status
    total = tickets.count()
    abertos = tickets.filter(status='Aberto').count()
    andamento = tickets.filter(status='Em andamento').count()
    resolvidos = tickets.filter(status='Resolvido').count()

    return render(request, 'tecnico_painel.html', {
        'tickets': tickets,
        'total': total,
        'abertos': abertos,
        'andamento': andamento,
        'resolvidos': resolvidos,
    })


