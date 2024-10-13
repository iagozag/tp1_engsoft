from django import forms
from .models import Usuario
from .models import Veiculo
class UsuarioForm(forms.ModelForm):
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
    email = forms.CharField(label = "Email", max_length=50)
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
    email = forms.CharField(label = 'Digite o novo e-mail', max_length=50)

class DeletaForm(forms.Form):
    senha = forms.CharField(label = 'Confirme a sua senha', max_length=128)
