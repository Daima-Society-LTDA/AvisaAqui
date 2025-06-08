from django.contrib import admin
from appHome.models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
        # Campos que você quer exibir na lista do admin
    list_display = ('id','nome_usuario', 'email', 'senha')

    list_filter = ('id', 'nome_usuario')

    search_fields = ('nome_usuario', 'email')

admin.site.register(Usuario, UsuarioAdmin)