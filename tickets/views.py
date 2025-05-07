from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import TicketForm
from .models import Ticket, LogChamado

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
    chamados_abertos = Ticket.objects.filter(usuario=request.user).exclude(status='Resolvido')
    chamados_resolvidos = Ticket.objects.filter(usuario=request.user, status='Resolvido')
    return render(request, 'usuario_dashboard.html', {
        'chamados_abertos': chamados_abertos,
        'chamados_resolvidos': chamados_resolvidos
    })
@login_required
def dashboard_tech(request):
    if not request.user.is_staff:
        return redirect('usuario_dashboard')  # Protege contra acesso indevido

    tickets = Ticket.objects.all().order_by('-criado_em')

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

@login_required
def detalhes_chamado(request, chamado_id):
    chamado = get_object_or_404(Ticket, id=chamado_id)
    tecnicos = User.objects.filter(profile__is_technician=True)

    historico = LogChamado.objects.filter(chamado=chamado).order_by('-data')

    if request.method == 'POST':
        status_antigo = chamado.status
        tecnico_antigo = chamado.tecnico_responsavel

        novo_status = request.POST.get('status')
        chamado.status = novo_status

        tecnico_id = request.POST.get('tecnico')
        if tecnico_id:
            chamado.tecnico_responsavel = User.objects.get(id=tecnico_id)

        nota = request.POST.get('nota')
        if nota:
            chamado.descricao_tecnico = nota

        chamado.save()

        # Log de status
        if status_antigo != chamado.status:
            LogChamado.objects.create(
                chamado=chamado,
                usuario=request.user,
                acao=f"Alterou status de '{status_antigo}' para '{chamado.status}'."
            )

        # Log de técnico
        if tecnico_antigo != chamado.tecnico_responsavel:
            LogChamado.objects.create(
                chamado=chamado,
                usuario=request.user,
                acao=f"Atribuiu o chamado ao técnico {chamado.tecnico_responsavel.username}."
            )

        # Log de nota
        if nota:
            LogChamado.objects.create(
                chamado=chamado,
                usuario=request.user,
                acao=f"Adicionou nota técnica."
            )

        return redirect('detalhes_chamado', chamado_id=chamado.id)

    return render(request, 'detalhes_chamado.html', {
        'chamado': chamado,
        'tecnicos': tecnicos,
        'historico': historico
    })
@login_required
def detalhes_chamado_usuario(request, chamado_id):
    chamado = get_object_or_404(Ticket, id=chamado_id, usuario=request.user)
    logs = chamado.logs.order_by('-data')

    return render(request, 'detalhes_user.html', {
        'chamado': chamado,
        'logs': logs
    })