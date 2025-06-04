from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar-usuario', views.cadastrar_usuario, name="cadastro_usuario"),
    path('login', views.login, name='login')
]