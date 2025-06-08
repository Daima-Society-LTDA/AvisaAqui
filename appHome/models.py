from django.db import models

# Create your models here.

class Usuario(models.Model):
    nome_usuario = models.CharField(max_length=45, unique=True)
    email = models.CharField(max_length=120, unique=True)
    senha = models.CharField(max_length=25)
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.nome_usuario

class Bairro(models.Model):
    nome = models.CharField(max_length=60)

    def __str__(self):
        return self.nome
    
class Ocorrencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='ocorrencias')
    titulo = models.CharField(max_length=120)
    descricao = models.TextField()
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE,  related_name='bairros')
    data_ocorrencia = models.DateTimeField(auto_now_add=True)

class Comentario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='comentarios_feitos')
    ocorrencia = models.ForeignKey(Ocorrencia, on_delete=models.CASCADE, related_name='comentarios')
    descricao_comentario = models.TextField()
    data_comentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_comentario']

    def __str__(self):
        return f"Comentário de {self.usuario.nome_usuario} em '{self.ocorrencia.titulo[:30]}"