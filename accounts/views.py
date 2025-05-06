from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirecionar de acordo com o tipo de usuário
            if hasattr(user, 'profile') and user.profile.is_technician:
                return redirect('painel_tecnico')  # nome da URL para técnicos
            else:
                return redirect('dashboard_usuario')  # nome da URL para usuários comuns
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



# @login_required
# def dashboard_usuario(request):
#     return render(request, 'usuario_dashboard.html')

# @login_required
# def painel_tecnico(request):
#     return render(request, 'tecnico_painel.html')
