from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import UsuarioForm
from .forms import VeiculoForm, CompletaForm
from django.http import HttpResponse
from .models import Usuario, Veiculo
from .forms import LoginForm

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data['email']
            request.session['senha'] = form.cleaned_data['senha']
            
            return redirect('completa')  # Redireciona para a página inicial ou outra página de sucesso
  # Redireciona para a página inicial ou outra página de sucesso
    else:
        form = UsuarioForm()
    
    return render(request, 'mysite/cadastro.html', {'form': form})

def completar_cadastro(request):
    if request.method == 'POST':
        form = CompletaForm(request.POST)
        if form.is_valid():
            email_usuario = request.session.get('email')
            senha_usuario = request.session.get('senha')
            usuario = form.save(commit = False)  # Salva no banco de dados SQLite
            usuario.email = email_usuario
            usuario.senha = senha_usuario
            usuario.save()
            
            request.session['cpf'] = usuario.cpf
            
            del request.session['email']
            del request.session['senha']
            
            e_motorista = form.cleaned_data['e_motorista']
            if e_motorista == 'sim':
                request.session['usuario'] = form.cleaned_data
                return redirect('veiculo') 
            return redirect('home')  # Redireciona para a página inicial ou outra página de sucesso
  # Redireciona para a página inicial ou outra página de sucesso
    else:
        form = CompletaForm()
    
    return render(request, 'mysite/cadastro.html', {'form': form})


def cadastrar_veiculo(request):
    if 'cpf' not in request.session:
        return redirect('cadastrar_usuario')
    
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit = False)  # Salva no banco de dados SQLite
            cpf_usuario = request.session['cpf']
            usuario = Usuario.objects.get(cpf=cpf_usuario)
            veiculo.cpf_motorista = usuario
            veiculo.save()
            del request.session['cpf']
            return redirect('home')  # Redireciona para a página inicial ou outra página de sucesso
    else:
        form = VeiculoForm()
    
    return render(request, 'mysite/cadastrarveiculo.html', {'form': form})

def home(request):
    return render(request, 'mysite/home.html')

from django.contrib.auth.hashers import check_password 

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            try:
                usuario = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                return HttpResponse("Email inválido!")

            if senha == usuario.senha:
                request.session['usuario_id'] = usuario.cpf
                return redirect('home') 
            return HttpResponse("Senha incorreta!")
    form = LoginForm()

    return render(request, 'mysite/login.html', {'form': form})
