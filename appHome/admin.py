from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
        # Campos que você quer exibir na lista do admin
    list_display = ('username', 'email', 'is_staff', 'is_active')

    list_filter = ('is_staff', 'is_active', 'groups')

    # Campos para pesquisa
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        (('Informações Adicionais'), {'fields': ('foto', 'descricao')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (('Informações Adicionais'), {'fields': ('foto', 'descricao')}),
    )