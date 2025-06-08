from django.contrib import admin
from appHome.models import Usuario, Bairro, Ocorrencia

class UsuarioAdmin(admin.ModelAdmin):
        # Campos que você quer exibir na lista do admin
    list_display = ('id','nome_usuario', 'email', 'senha')

    list_filter = ('id', 'nome_usuario')

    search_fields = ('nome_usuario', 'email')

class OcorrenciaAdmin(admin.ModelAdmin):
        # Campos que você quer exibir na lista do admin
    list_display = ('id','titulo', 'descricao', 'data_ocorrencia', 'bairro')

    list_filter = ('id', 'data_ocorrencia')

    search_fields = ('titulo', 'data_ocorrencia')

class BairroAdmin(admin.ModelAdmin):
    list_display = ('id','nome')

    list_filter = ('id', 'nome')

    search_fields = ('id', 'nome')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Ocorrencia, OcorrenciaAdmin)
admin.site.register(Bairro, BairroAdmin)