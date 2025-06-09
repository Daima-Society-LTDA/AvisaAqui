from appHome.forms import UsuarioForm, UsuarioLoginForm, OcorrenciaForm, ComentarioForm
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.templatetags.static import static
from django.utils import timezone

from .models import Usuario, Ocorrencia

def home(request):
    form_ocorrencia = OcorrenciaForm()
    usuario_logado = None
    if 'email' in request.session:
        try:
            usuario_logado = Usuario.objects.get(email=request.session['email'])
        except Usuario.DoesNotExist:
            request.session.flush()
            return redirect('login')

    if request.method == 'POST':
        if 'titulo' in request.POST and 'descricao' in request.POST: 
            form_ocorrencia = OcorrenciaForm(request.POST)
            if form_ocorrencia.is_valid():
                if usuario_logado:
                    ocorrencia = form_ocorrencia.save(commit=False)
                    ocorrencia.usuario = usuario_logado
                    ocorrencia.save()
                    
                    return redirect('home')
                else:
                    form_ocorrencia.add_error(None, "Você precisa estar logado para postar uma ocorrência.")
            
    ocorrencias = Ocorrencia.objects.all().order_by('-data_ocorrencia')
    
    dados = {
        'form_ocorrencia': form_ocorrencia,
        'usuario_logado': usuario_logado,
        'ocorrencias': ocorrencias,
    }
    return render(request, 'home.html', dados)

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
                    request.session.set_expiry(timedelta(minutes=15))
                    request.session['email'] = _email
                    request.session['nome'] = usuario_login.nome_usuario
                    if usuario_login.foto:
                        request.session["foto_perfil_url"] = usuario_login.foto.url
                    else:
                        request.session["foto_perfil_url"] = static('img/icon-user.png')
                    return redirect("home")
            except Usuario.DoesNotExist:
                formLogin.add_error(None, "Email ou senha inválidos.")
                
            return render(request, 'login.html', {'formLogin': formLogin})
        
    return render(request, 'login.html', {'formLogin': formLogin})

def logout(request):
    request.session.flush()
    return redirect("login")

@require_GET
def get_comentarios_ocorrencia(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, pk=ocorrencia_id)
    comentarios = ocorrencia.comentarios.all().order_by('data_comentario')
    
    comentarios_data = []
    for comentario in comentarios:
        comentarios_data.append({
            'descricao': comentario.descricao_comentario,
            'usuario_nome': comentario.usuario.nome_usuario,
            'data': comentario.data_comentario.strftime("%d/%m/%Y %H:%M"), # Formata a data
            'usuario_foto_url': comentario.usuario.foto.url if comentario.usuario.foto else static('/img/icon-user.png') # Adapte para o seu campo de foto
        })
    
    return JsonResponse({'comentarios': comentarios_data})

@require_POST # Esta view só aceita requisições POST
def adicionar_comentario(request, ocorrencia_id):
    ocorrencia = get_object_or_404(Ocorrencia, pk=ocorrencia_id)
    usuario_logado = None

    if 'email' in request.session:
        try:
            usuario_logado = Usuario.objects.get(email=request.session['email'])
        except Usuario.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'Usuário não logado.'}, status=401)
    else:
        return JsonResponse({'success': False, 'errors': 'Você precisa estar logado para comentar.'}, status=401)

    form_comentario = ComentarioForm(request.POST)
    if form_comentario.is_valid():
        comentario = form_comentario.save(commit=False)
        comentario.ocorrencia = ocorrencia
        comentario.usuario = usuario_logado
        comentario.save()

        data_local_comentario = timezone.localtime(comentario.data_comentario)

        response_data = {
            'success': True,
            'comentario': {
                'descricao': comentario.descricao_comentario,
                'usuario_nome': comentario.usuario.nome_usuario,
                'data': data_local_comentario.strftime("%d/%m/%Y %H:%M"),
                'usuario_foto_url': comentario.usuario.foto.url if comentario.usuario.foto else static('img/icon-user.png')
            }
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'errors': form_comentario.errors.as_json()}, status=400) # Retorna erros do formulário