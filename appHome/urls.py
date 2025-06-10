from django.urls import path

from appHome import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar-usuario', views.cadastrar_usuario, name="cadastro_usuario"),
    path('login', views.login_view, name='login'),
    path('logout', views.logout, name="logout"),
    path('ocorrencias/<int:ocorrencia_id>/comentarios/', views.get_comentarios_ocorrencia, name='get_comentarios_ocorrencia'),
    path('ocorrencias/<int:ocorrencia_id>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
    path('perfil/<int:cd_usuario>', views.perfil, name="perfil"),
    path('editar-perfil/<int:cd_usuario>', views.editar_perfil, name="editar_perfil"),
    path('excluir-conta/<int:cd_usuario>', views.excluir_conta, name="excluir_conta")
]