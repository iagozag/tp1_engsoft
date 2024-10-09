from django.db import models

# Create your models here.
class Usuario(models.Model):
    nome = models.CharField(max_length=100,default='')
    cpf = models.CharField(max_length=11, primary_key=True)  # CPF único do usuário
    email = models.EmailField(unique=True)  # Email único do usuário
    data_nascimento = models.CharField(max_length=100)  # Data de nascimento do usuário
    telefone = models.CharField(max_length=15, blank=True, null=True)  # Telefone do usuário
    avaliacao_media = models.FloatField(default=0)  # Média de avaliações
    senha = models.CharField(max_length=128)  # Senha do usuário (use hashing na prática)

    def _str_(self):
        return self.cpf  # Retorna o email como representação do usuário
    
# usuarios/models.py
from django.db import models

class Carona(models.Model):
    cpf_motorista = models.ForeignKey('Usuario', on_delete=models.CASCADE)  # Chave estrangeira para Usuario
    quantidade = models.IntegerField()
    veiculo = models.ForeignKey('Veiculo', on_delete=models.CASCADE)  # Chave estrangeira para Veiculo
    ponto_encontro = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    data_hora = models.DateTimeField()  # Campo para data e hora

    def _str_(self):
        return f'Carona {self.id} - Motorista: {self.cpf_motorista}'
    
# usuarios/models.py
class Historico(models.Model):
    numero_carona = models.ForeignKey(Carona, on_delete=models.CASCADE)  # Chave estrangeira para Carona
    cpf_motorista = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='historico_motorista')  # Chave estrangeira para Usuario
    cpf_usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='historico_usuario')  # Chave estrangeira para Usuario
    avaliacao_motorista = models.IntegerField(null=True, blank=True)  # Avaliação do motorista
    avaliacao_usuario = models.IntegerField(null=True, blank=True)  # Avaliação do usuário

    class Meta:
        unique_together = (('numero_carona', 'cpf_usuario'),)  # Chave primária composta

    def _str_(self):
        return f'Historico - Carona {self.numero_carona} - Usuário: {self.cpf_usuario}'

class Veiculo(models.Model):
    cpf_motorista = models.ForeignKey('Usuario', on_delete=models.CASCADE, default='0.00000000')  # Chave estrangeira para Usuario
    placa = models.CharField(max_length=7, primary_key=True)  # A placa será a chave primária, portanto, deve ser única
    modelo = models.CharField(max_length=50)  # Campo para o modelo do veículo
    cor = models.CharField(max_length=20)  # Campo para a cor do veículo

    def _str_(self):
        return f'{self.modelo} ({self.placa})'
    
    