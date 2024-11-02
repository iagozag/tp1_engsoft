from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm
from .forms import VeiculoForm, CompletaForm, CaronaForm
from django.http import HttpResponse
from .models import Usuario, Veiculo, Carona
from .forms import LoginForm, NomeForm, SenhaForm, DataForm, EmailForm, TelefoneForm, DeletaForm, CaronaForm
from django.contrib.auth import logout
from .forms import ConfirmacaoCancelamentoForm
from django.http import JsonResponse
from datetime import datetime

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            request.session['email'] = form.cleaned_data['email']
            request.session['senha'] = form.cleaned_data['senha']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})
    else:
        form = UsuarioForm()
        completa_form = CompletaForm()
        veiculo_form = VeiculoForm()

    return render(request, 'mysite/cadastro.html', {'form': form, 'completa_form': completa_form, 'veiculo_form': veiculo_form})

def completar_cadastro(request):
    if request.method == 'POST':
        form = CompletaForm(request.POST)
        if form.is_valid():
            e_motorista = form.cleaned_data['e_motorista']

            request.session['cpf'] = form.cleaned_data['cpf']
            request.session['nome'] = form.cleaned_data['nome']
            request.session['data_nascimento'] = form.cleaned_data['data_nascimento']
            request.session['telefone'] = form.cleaned_data['telefone']
            
            if e_motorista:
                return JsonResponse({'success': True, 'redirect': 'veiculo'})

            usuario = Usuario(
                cpf=request.session['cpf'],
                email=request.session['email'],
                senha=request.session['senha'],
                data_nascimento=request.session['data_nascimento'],
                telefone=request.session['telefone'],
            )
            usuario.save()
            del request.session['email'], request.session['senha'], request.session['data_nascimento'], request.session['telefone']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})

def cadastrar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit=False)

            usuario = Usuario(
                cpf=request.session['cpf'],
                email=request.session['email'],
                senha=request.session['senha'],
                data_nascimento=request.session['data_nascimento'],
                telefone=request.session['telefone'],
            )
            usuario.save()

            veiculo.cpf_motorista = usuario
            veiculo.save()

            del request.session['email'], request.session['senha'], request.session['data_nascimento'], request.session['telefone']
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})


def home(request):
    # print(Carona.objects.values())
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
                # eu (manuel) mudei pq as verificações estavam requisitando o cpf na sessão
                # só comentado pra evitar o risco de eu ter feito algo errado
                # request.session['usuario_id'] = usuario.cpf
                request.session['cpf'] = usuario.cpf

                return redirect('home')
            return HttpResponse("Senha incorreta!")
    form = LoginForm()

    return render(request, 'mysite/login.html', {'form': form})

def logout_usuario(request):
    try:
        del request.session['cpf']
    except KeyError:
        pass
    return redirect('home')


def configuracoes(request):
    if 'cpf' not in request.session: return redirect('cadastrar_usuario')
    
    cpf = request.session['cpf']

    motorista = Veiculo.objects.filter(cpf_motorista=cpf).exists()
    
    usuario = Usuario.objects.get(cpf=cpf)

    d = {'formnome'     : NomeForm(),
         'formdata'     : DataForm(),
         'formtel'      : TelefoneForm(),
         'formsen'      : SenhaForm(),
         'formemail'    : EmailForm(),
         'formdel'      : DeletaForm(),
         'eh_motorista' : motorista,
         'nome'         : usuario.nome,
         'data'         : datetime.strptime(usuario.data_nascimento,"%d/%m/%Y").strftime("%d/%m/%Y"),
         'tel'          : usuario.telefone,
         'email'        : usuario.email
        }
    
    if request.method == 'POST':
        formData = DataForm(request.POST)
        formNome = NomeForm(request.POST)
        formTel = TelefoneForm(request.POST)
        alterou = False

        if 'cadastra' in request.POST: return redirect('veiculo')
        
        if 'descadastra_veiculo' in request.POST:
            Veiculo.objects.filter(cpf_motorista = cpf).delete()
            return HttpResponse('Veĩculo descadastrado com sucesso')

        if formNome.has_changed():
            if formNome.is_valid():
                print('nome')
                alterou = True
                novoNome = formNome.cleaned_data['nome']
                user = Usuario.objects.get(cpf=cpf)
                user.nome = novoNome
                user.save()

        if formData.has_changed():
            if formData.is_valid():
                print('data')
                alterou = True
                novaData = formData.cleaned_data['data']
                user = Usuario.objects.get(cpf=cpf)
                user.data_nascimento = novaData
                user.save()
            else: return HttpResponse(formData.s)

        if formTel.has_changed() :
            if formTel.is_valid():
                print('tel')
                alterou = True
                novoTel = formTel.cleaned_data['telefone']
                user = Usuario.objects.get(cpf=cpf)
                user.telefone = novoTel
                user.save()
        if alterou: return HttpResponse("informações atualizadas com sucesso")

        formSenha = SenhaForm(request.POST)
        if formSenha.is_valid():
            senhaAtual, novaSenha = formSenha.cleaned_data['senhaAtual'], formSenha.cleaned_data['novaSenha']
            user = Usuario.objects.get(cpf=cpf)
            if senhaAtual!=user.senha: return HttpResponse("Senha incorreta!")
            user.senha = novaSenha
            user.save()
            return HttpResponse('Senha alterada com sucesso')

        formEmail = EmailForm(request.POST)
        if formEmail.is_valid():
            email = formEmail.cleaned_data['email']
            user = Usuario.objects.get(cpf=cpf)
            user.email = email
            user.save()
            return HttpResponse('Email alterado com sucesso')

        formDel = DeletaForm(request.POST)
        if formDel.is_valid():
            senha = formDel.cleaned_data['senha']
            user = Usuario.objects.get(cpf=cpf)
            if senha!=user.senha: return HttpResponse("Senha incorreta!")
            logout(request)
            user.delete()
            return redirect('cadastrar_usuario')
            

    return render(request, 'mysite/configuracoes.html',d)

import requests
from requests.structures import CaseInsensitiveDict

url = "https://api.geoapify.com/v1/geocode/autocomplete?text=Mosco&apiKey=643e0f44a71c43dd978997ddc8ce67ff"

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"

resp = requests.get(url, headers=headers)

print(resp.status_code)

def criar_carona(request):
    if 'cpf' not in request.session: return redirect('cadastrar_usuario')
    
    cpf = request.session['cpf']
    try: veiculo = Veiculo.objects.get(cpf_motorista = cpf)
    except Veiculo.DoesNotExist: return HttpResponse("Veículo não cadastrado")
        
    if request.method == 'POST':
        form = CaronaForm(request.POST)
        if form.is_valid():
            qtd = form.cleaned_data['quantidade']
            ponto_encontro = form.cleaned_data['ponto_encontro']
            destino = form.cleaned_data['destino']
            data_hora = form.cleaned_data['data_hora']

            carona = Carona()
            carona.cpf_motorista = Usuario.objects.get(cpf=cpf)
            carona.quantidade = qtd
            carona.veiculo = veiculo
            carona.ponto_encontro = ponto_encontro
            carona.destino = destino
            carona.data_hora = data_hora
            
            carona.save()
            return HttpResponse("Carona criada com sucesso")
        else: return HttpResponse(form.s)

    return render(request, 'mysite/criarcarona.html', {'form':CaronaForm()})

def visualizar_caronas(request):
    #eu vou estar logada e eu quero ver minhas caronas OFERECIDAS
    cpf = request.session['cpf']
    try: veiculo = Veiculo.objects.get(cpf_motorista = cpf)
    except Veiculo.DoesNotExist : return HttpResponse("Nenhum veículo cadastrado nesse CPF")

    caronas = Carona.objects.filter(cpf_motorista = cpf)

    return render(request, 'mysite/visualizarcaronas.html', {'caronas': caronas})

def editar_carona(request, carona_id):
    carona = get_object_or_404(Carona, id=carona_id)
    #forms modelo forms.Form --> exige que usemos o processo manual == não pode usar instance
    if request.method == 'POST':
        form = CaronaForm(request.POST)
        if form.is_valid():
            carona.quantidade = form.cleaned_data['quantidade']
            carona.ponto_encontro = form.cleaned_data['ponto_encontro']
            carona.destino = form.cleaned_data['destino']
            carona.data_hora = form.cleaned_data['data_hora']
            carona.save()
            return redirect('visualizar_caronas')
    else:
        form = CaronaForm(initial={
            'quantidade': carona.quantidade,
            'ponto_encontro': carona.ponto_encontro,
            'destino': carona.destino,
            'data_hora': carona.data_hora,
        })
    
    return render(request, 'mysite/editar_carona.html', {'form': form, 'carona': carona})

def cancelar_carona(request, carona_id):
    carona = get_object_or_404(Carona, id=carona_id)

    if request.method == 'POST':
        carona.delete()
        return redirect('visualizar_caronas')

def listar_caronas(request):
    destino = request.GET.get('Destino')
    data = request.GET.get('data')
    caronas =  Carona.objects.none()
    
    print("Destino: ",destino)
    print("Data: ",data)
    
    
    if destino and data:
        try:
            data_formatado = datetime.strptime(data, '%Y-%m-%d').date()
            caronas =  Carona.objects.all()
            caronas = caronas.filter(destino__iexact = destino, data_hora__date=data_formatado)
            print("caronas encontradas", caronas)
        except ValueError:
            pass
        

    return render(request, 'mysite/consulta.html', {'caronas':caronas})