from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome = models.CharField(max_length=70)
    email = models.EmailField(max_length=120,unique=True)
    senha = models.CharField(max_length=45)
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome
