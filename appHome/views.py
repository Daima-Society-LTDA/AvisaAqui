from django.shortcuts import render, redirect
from .forms import UsuarioForm, UsuarioLoginForm

from .models import Usuario

from datetime import timedelta

# Create your views here.
def home(request):
    return render(request, 'home.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # ou redirecione para onde quiser
    else:
        form = UsuarioForm()
    return render(request, 'cadastro_usuario.html', {'form': form})

def login(request):
    frmLogin = UsuarioLoginForm(request.POST or None)

    if request.POST:
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get("email")
            _senha = frmLogin.cleaned_data.get("senha") 

            try:
                userLogin = Usuario.objects.get(email=_email, senha=_senha) 
                if userLogin is not None:
                    request.session.set_expiry(timedelta(minutes=15))
                    request.session['email'] = _email
                    request.session['nome'] = userLogin.nome
                    return redirect("home")
            except Usuario.DoesNotExist:
                frmLogin.add_error(None, "Usuário ou senha inválidos")
            
    return render(request, "login.html", {'form' : frmLogin})