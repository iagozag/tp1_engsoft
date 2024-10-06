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
        
    e_motorista = forms.ChoiceField(
        choices=[('sim', 'Sim'), ('nao', 'Não')],
        widget=forms.RadioSelect(),
        label="Você é um motorista?"
    )
    
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['placa','modelo', 'cor'] 
   
        