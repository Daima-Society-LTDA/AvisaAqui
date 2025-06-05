from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    descricao = models.TextField(blank=True)

    # Adicione ESTAS LINHAS para resolver os erros de related_name
    # Estes são os campos groups e user_permissions, herdados de AbstractUser,
    # mas com related_name e related_query_name personalizados para evitar conflitos.
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="apphome_user_set", # <--- NOME ÚNICO AQUI!
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="apphome_user_permissions", # <--- NOME ÚNICO AQUI!
        related_query_name="user",
    )

    def __str__(self):
        return self.username

class Ocorrencia(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    # adiciona a data e hora atual
    data_postagem = models.DateTimeField(auto_now_add=True)
    bairro_ocorrencia = models.CharField(max_length=80)

    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ocorrencia"
        ordering = ['-data_postagem']

    def __str__(self):
        return self.titulo