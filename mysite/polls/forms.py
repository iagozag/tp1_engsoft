from django import forms
from .models import Usuario
from .models import Veiculo
from django.utils import timezone
from datetime import timedelta

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['email', 'senha']


class CompletaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']

    e_motorista = forms.BooleanField(
        required=False,
        label="Você é um motorista?"
    )

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','modelo', 'cor']

class LoginForm(forms.Form):
    email = forms.EmailField(label = "Email", max_length=50)
    senha = forms.CharField(widget=forms.PasswordInput)

class NomeForm(forms.Form):
    nome = forms.CharField(label = 'Nome' ,max_length=100)

class DataForm(forms.Form):
    data = forms.CharField(label = 'Data de nascimento' ,max_length=100)

class TelefoneForm(forms.Form):
    telefone = forms.CharField(label = 'Novo número de telefone' ,max_length=15)

class SenhaForm(forms.Form):
    senhaAtual = forms.CharField(label = 'Digite sua senha' ,max_length=128)
    novaSenha = forms.CharField(label = 'Digite sua nova senha', max_length=128)

class EmailForm(forms.Form):
    email = forms.EmailField(label = 'Digite o novo e-mail', max_length=50)

class DeletaForm(forms.Form):
    senha = forms.CharField(label = 'Confirme a sua senha', max_length=128)

class CaronaForm(forms.Form):
    escolhas = [(1,'1'),
                (2,'2'),
                (3,'3'),
                (4,'4')]
    
    quantidade = forms.ChoiceField(choices=escolhas,label='Número de vagas')
    ponto_encontro = forms.CharField(label='Ponto de encontro', max_length=128)
    destino = forms.CharField(label='Destino',max_length=128)
    data_hora = forms.DateTimeField(
        label='Data e horário de partida',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%d/%m/%Y %h:%M']
        )
    
    def clean_data_hora(self):
        data_hora = self.cleaned_data['data_hora']

        if data_hora <= timezone.now() + timedelta(hours=2):
            self.s = "A data e hora precisam ser, ao menos, duas horas a partir de agora."
            raise forms.ValidationError(self.s)
        
        if data_hora >= timezone.now() + timedelta(weeks=2):
            self.s = 'A carona deve ser criada com, no máximo, duas semanas de antecedência.'
            raise forms.ValidationError(self.s)
        return data_hora

class ConfirmacaoCancelamentoForm(forms.Form):
    confirmar = forms.BooleanField(label = 'Você tem certeza que deseja cancelar essa carona?', required=True, widget = forms.HiddenInput())
