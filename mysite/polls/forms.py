from django import forms
from .models import Usuario
from .models import Veiculo
from django.utils import timezone
from datetime import timedelta, date

class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario
        fields = ['email', 'senha']


class CompletaForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'cpf', 'data_nascimento', 'telefone']
        widgets = {
            'data_nascimento': forms.DateInput(format='%d/%m/%Y', attrs={'type':'date','placeholder': 'dd/mm/yyyy'}),
        }

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
    nome = forms.CharField(label = 'Novo nome' ,max_length=100,required=True)

class DataForm(forms.Form):
    data = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        label = 'Nova data de nascimento',
        widget=forms.DateInput(
            attrs={'type' : 'date', 'placeholder': 'dd/mm/yyyy'},
            format='%Y/%m/%d'),
        required=True
    )
    
    def clean_data(self):
        m = date.today() - timedelta(days=13*365)
        d = self.cleaned_data['data']

        if d > m:
            raise forms.ValidationError('Você deve ter ao menos 13 anos para utilizar o sistema')
        return d

class TelefoneForm(forms.Form):
    telefone = forms.CharField(label = 'Novo número de telefone' ,
                               max_length=15,
                               required=True)

class SenhaForm(forms.Form):
    senhaAtual = forms.CharField(
        label = 'Digite sua senha atual',
        max_length=128,required=True,
        widget=forms.PasswordInput
    )
    novaSenha = forms.CharField(
        label = 'Digite sua nova senha',
        max_length=128,
        required=True,
        widget=forms.PasswordInput
    )

class EmailForm(forms.Form):
    email = forms.EmailField(label = 'Digite o novo e-mail',max_length=50,required=True)

class DeletaForm(forms.Form):
    senha = forms.CharField(
        label = 'Confirme a sua senha',
        max_length=128,
        required=True,
        widget=forms.PasswordInput)

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
