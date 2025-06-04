from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha', 'foto', 'descricao']

        widgets = {
            'nome' : forms.TextInput(attrs={'type':'text', 'class':'form-input'}),
            'email' : forms.TextInput(attrs={'type':'email', 'class':'form-input'}),
            'cep' : forms.TextInput(attrs={'type':'text', 'class': 'form-input'}),
            'senha' : forms.TextInput(attrs={'type':'password', 'class':'form-input'}),
            'descricao' : forms.TextInput(attrs={'type':'text', 'class':'form-input'}),
            'imagem' : forms.FileInput(attrs={'accept': 'image/*'})
        }

class UsuarioLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'type': 'email', 'class': 'form-input'})
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'type': 'password', 'class': 'form-input'})
    )