from django.urls import path

from appHome import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastrar-usuario', views.cadastrar_usuario, name="cadastro_usuario"),
    path('login', views.login_view, name='login'),
    path('logou', views.logout, name="logout")
]