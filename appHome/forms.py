from django import forms
from appHome.models import Usuario, Ocorrencia, Comentario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_usuario', 'email', 'descricao', 'senha', 'foto',)

        widgets = {
            'nome_usuario': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'foto': forms.FileInput(attrs={'accept': 'image/*', 'class': 'input'}),
            'descricao': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
        }

    # Senha e Confirmação de Senha separadas para segurança e validação
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )

    # Validação customizada para garantir que as senhas são iguais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('senha')
        password_confirm = cleaned_data.get('confirmar_senha')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")
        return cleaned_data

class UsuarioLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'input'})
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )

class UsuarioEditForm(forms.ModelForm):
    senha = forms.CharField(
        label="Nova Senha (deixe em branco para não alterar)",
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Nova Senha",
        required=False, # Confirmação também não é obrigatória
        widget=forms.PasswordInput(attrs={'class': 'input'})
    )

    class Meta:
        model = Usuario
        fields = ('nome_usuario', 'email', 'descricao', 'foto', 'senha') 
        
        widgets = {
            'nome_usuario': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'foto': forms.FileInput(attrs={'accept': 'image/*', 'class': 'input'}),
            'descricao': forms.Textarea(attrs={'class': 'textarea', 'rows': 4}),
        }

    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('senha')
        confirm_senha = cleaned_data.get('confirmar_senha')

        if nova_senha:
            if nova_senha and confirm_senha and nova_senha != confirm_senha:
                self.add_error('confirmar_senha', "As novas senhas não coincidem.")
            elif not confirm_senha:
                self.add_error('confirmar_senha', "Por favor, confirme sua nova senha.")
        elif confirm_senha:
             self.add_error('senha', "Por favor, digite sua nova senha para confirmá-la.")
             
        return cleaned_data

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ('titulo', 'descricao', 'bairro')
        widgets = {
            'titulo' : forms.TextInput(attrs={'class': 'input'}),
            'descricao': forms.Textarea(attrs={'class': 'textarea'}),
        }
    
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ('descricao_comentario', )
        widgets = {
            'descricao_comentario' : forms.Textarea(attrs={'class': 'textarea', 'rows' : 3})
        }