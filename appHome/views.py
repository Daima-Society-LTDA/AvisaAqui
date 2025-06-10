from appHome.forms import UsuarioEditForm, UsuarioForm, UsuarioLoginForm, OcorrenciaForm, ComentarioForm
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.templatetags.static import static
from django.utils import timezone
from rest_framework import generics
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from appHome.serializers import OcorrenciaSerializer

from .models import Usuario, Ocorrencia

def home(request):
    usuario_logado = None
    if 'email' in request.session:
        try:
            usuario_logado = Usuario.objects.get(email=request.session['email'])
        except Usuario.DoesNotExist:
            request.session.flush()

    form_ocorrencia = OcorrenciaForm()

    if request.method == 'POST':
        if usuario_logado:
            form_ocorrencia = OcorrenciaForm(request.POST)
            if form_ocorrencia.is_valid():
                ocorrencia = form_ocorrencia.save(commit=False)
                ocorrencia.usuario = usuario_logado
                ocorrencia.save()
                return redirect('home')
        else:
            return redirect('login')


    todas_ocorrencias = Ocorrencia.objects.all().order_by('-data_ocorrencia') 

    paginator = Paginator(todas_ocorrencias, 5) 

    page = request.GET.get('page')

    try:
        ocorrencias = paginator.page(page)
    except PageNotAnInteger:
        ocorrencias = paginator.page(1)
    except EmptyPage:
        ocorrencias = paginator.page(paginator.num_pages)

    dados = {
        'form_ocorrencia': form_ocorrencia,
        'ocorrencias': ocorrencias,
        'usuario_logado': usuario_logado
    }
    return render(request, "home.html", dados)

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
                    request.session.set_expiry(timedelta(minutes=30))
                    request.session['cd_usuario'] = usuario_login.id
                    request.session['descricao'] = usuario_login.descricao
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
        return JsonResponse({'success': False, 'errors': form_comentario.errors.as_json()}, status=400)
    
def perfil(request, cd_usuario):
    if 'email' in request.session:
        usuario_logado = Usuario.objects.get(id=cd_usuario)

        if usuario_logado.foto:
            foto_url = usuario_logado.foto.url
        else:
            foto_url = static('/img/icon-user.png')
        
        dados = {
            'nome' : usuario_logado.nome_usuario,
            'email' : usuario_logado.email,
            'descricao' : usuario_logado.descricao,
            'foto' : foto_url
        }
        print(dados['foto'])
        return render(request, "perfil.html", dados)

    return redirect("home")

def editar_perfil(request, cd_usuario):
    if 'email' not in request.session:
        return redirect("login")

    try:
        usuario_logado = Usuario.objects.get(email=request.session['email'])
    except Usuario.DoesNotExist:
        request.session.flush()
        return redirect('login')

    if usuario_logado.id != cd_usuario:
        return redirect("home")

    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, request.FILES, instance=usuario_logado)
        if form.is_valid():
            usuario = form.save(commit=False)
            nova_senha = form.cleaned_data.get('senha')
            if nova_senha:
                usuario.senha = nova_senha

            usuario.save()

            request.session['descricao'] = usuario.descricao
            request.session['nome'] = usuario.nome_usuario
            if usuario.foto:
                request.session["foto_perfil_url"] = usuario.foto.url
            else:
                request.session["foto_perfil_url"] = static('img/icon-user.png')

            return redirect('perfil', cd_usuario=usuario.id)
    else:
        form = UsuarioEditForm(instance=usuario_logado)

    if usuario_logado.foto:
        foto_url = usuario_logado.foto.url
    else:
        foto_url = static('img/icon-user.png')

    dados = {
        'form': form,
        'usuario': usuario_logado,
        'foto_perfil_url': foto_url,
    }
    return render(request, 'editar-perfil.html', dados)

def excluir_conta(request, cd_usuario):
    if 'email' not in request.session:

        return redirect("login")
    try:
        usuario_logado = Usuario.objects.get(email=request.session['email'])
    except Usuario.DoesNotExist:
        request.session.flush()
        
        return redirect('login')

    if usuario_logado.id != cd_usuario:
        messages.error(request, "Você não tem permissão para excluir esta conta.")
        return redirect("home")

    if request.method == 'POST':
        usuario_logado.delete()
        
        request.session.flush()
        
        return redirect('login')
    return redirect('perfil', cd_usuario=cd_usuario)

# API
# View para listar todas as ocorrências
class OcorrenciaListAPIView(generics.ListAPIView):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer

# View para pegar uma ocorrência específica pelo ID
class OcorrenciaDetailAPIView(generics.RetrieveAPIView):
    queryset = Ocorrencia.objects.all()
    serializer_class = OcorrenciaSerializer
    lookup_field = 'id'

# POR DATA
class OcorrenciaDoDiaListAPIView(generics.ListAPIView):
    serializer_class = OcorrenciaSerializer

    def get_queryset(self):
        today = timezone.now().date()
        queryset = Ocorrencia.objects.filter(data_ocorrencia__date=today)
        return queryset