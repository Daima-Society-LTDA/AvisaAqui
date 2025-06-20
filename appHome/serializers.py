from rest_framework import serializers
from .models import Ocorrencia

class OcorrenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ocorrencia
        fields = ['id', 'titulo', 'descricao', 'data_ocorrencia']