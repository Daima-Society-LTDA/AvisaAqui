from django import forms
from appHome.models import Usuario, Ocorrencia

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('nome_usuario', 'email', 'senha', 'descricao')

        widgets = {
            'nome_usuario': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'foto': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

    # Senha e Confirmação de Senha separadas para segurança e validação
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
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
        widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-input'})
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-input'})
    )

class OcorrenciaForm(forms.ModelForm):
    class Meta:
        model = Ocorrencia
        fields = ('titulo', 'descricao', 'bairro')
        widgets = {
            'titulo' : forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textArea'}),
        }