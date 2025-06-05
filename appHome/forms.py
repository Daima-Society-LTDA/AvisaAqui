from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    # Senha e Confirmação de Senha separadas para segurança e validação
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )
    password_confirm = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Usuario
        # Não inclua 'password' aqui, pois ele será tratado manualmente para hashing.
        # AbstractUser já tem 'username', 'email', 'first_name', 'last_name', etc.
        fields = ['username', 'email', 'foto', 'descricao']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'foto': forms.FileInput(attrs={'accept': 'image/*', 'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }

    # Validação customizada para garantir que as senhas são iguais
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "As senhas não coincidem.")
        return cleaned_data

    # Sobrescreve o método save para lidar com o hashing da senha
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"]) # Faz o hash da senha
        if commit:
            user.save()
        return user

class UsuarioLoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-input'})
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-input'})
    )