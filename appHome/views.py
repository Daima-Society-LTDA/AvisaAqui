from datetime import timedelta
from django.shortcuts import render, redirect
from appHome.forms import UsuarioForm, UsuarioLoginForm

from .models import Usuario

def home(request):
    return render(request, 'home.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redireciona para a home após o cadastro bem-sucedido
            return redirect('home')
    else:
        form = UsuarioForm()
    return render(request, 'cadastro_usuario.html', {'form': form})

def login_view(request):
    formLogin = UsuarioLoginForm(request.POST or None)

    if request.POST:
        if formLogin.is_valid():
            _email = formLogin.cleaned_data.get("email")
            _senha = formLogin.cleaned_data.get("senha")
            
            try:
                usuario_login = Usuario.objects.get(email=_email, senha=_senha)
                if usuario_login is not None:
                    request.session.set_expiry(timedelta(seconds=15))
                    request.session['email'] = _email
                    request.session['nome'] = usuario_login.nome_usuario
                    return redirect("home")
            except Usuario.DoesNotExist:
                formLogin.add_error(None, "Email ou senha inválidos.")
                
            return render(request, 'login.html', {'formLogin': formLogin})
        
    return render(request, 'login.html', {'formLogin': formLogin})

def logout(request):
    request.session.flush()
    return redirect("login")