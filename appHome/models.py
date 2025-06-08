from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome_usuario = models.CharField(max_length=45, unique=True)
    email = models.CharField(max_length=120, unique=True)
    senha = models.CharField(max_length=25)
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    descricao = models.TextField(blank=True)