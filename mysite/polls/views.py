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
        completa_form = CompletaForm()  # Adicionei isso aqui para o segundo formulário

    return render(request, 'mysite/cadastro.html', {'form': form, 'completa_form': completa_form})

def completar_cadastro(request):
    if request.method == 'POST':
        form = CompletaForm(request.POST)
        if form.is_valid():
            email_usuario = request.session.get('email')
            senha_usuario = request.session.get('senha')
            usuario = form.save(commit=False)
            usuario.email = email_usuario
            usuario.senha = senha_usuario
            usuario.save()

            request.session['cpf'] = usuario.cpf

            del request.session['email']
            del request.session['senha']

            e_motorista = form.cleaned_data['e_motorista']
            if e_motorista:
                return JsonResponse({'success': True, 'redirect': 'veiculo'})
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors})

    form = CompletaForm()
    return render(request, 'mysite/completa.html', {'form': form})


def cadastrar_veiculo(request):
    if 'cpf' not in request.session:
        return redirect('login')

    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            veiculo = form.save(commit = False)  # Salva no banco de dados SQLite
            cpf_usuario = request.session['cpf']
            usuario = Usuario.objects.get(cpf=cpf_usuario)
            veiculo.cpf_motorista = usuario
            veiculo.save()
            return redirect('home')  # Redireciona para a página inicial ou outra página de sucesso
    else:
        form = VeiculoForm()

    return render(request, 'mysite/veiculo.html', {'form': form})

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


def configuracoes(request):
    if 'cpf' not in request.session: return redirect('cadastrar_usuario')
    
    cpf = request.session['cpf']

    d = {'formnome' : NomeForm(),
         'formdata' : DataForm(),
         'formtel'  : TelefoneForm(),
         'formsen'  : SenhaForm(),
         'formemail': EmailForm(),
         'formdel'  : DeletaForm()
        }
    
    if request.method == 'POST':
        if 'cadastra' in request.POST: return redirect('veiculo')
        
        if 'descadastra_veiculo' in request.POST:
            Veiculo.objects.filter(cpf_motorista = cpf).delete()
            return redirect('login')

        formNome = NomeForm(request.POST)
        if formNome.is_valid():
            novoNome = formNome.cleaned_data['nome']
            user = Usuario.objects.get(cpf=cpf)
            user.nome = novoNome
            user.save()
            return render(request, 'mysite/configuracoes.html',d)


        formData = DataForm(request.POST)
        if formData.is_valid():
            novaData = formData.cleaned_data['data']
            user = Usuario.objects.get(cpf=cpf)
            user.data_nascimento = novaData
            user.save()
            return render(request, 'mysite/configuracoes.html',d)

        formTel = TelefoneForm(request.POST)
        if formTel.is_valid():
            novoTel = formTel.cleaned_data['telefone']
            user = Usuario.objects.get(cpf=cpf)
            user.telefone = novoTel
            user.save()
            return render(request, 'mysite/configuracoes.html',d)

        formSenha = SenhaForm(request.POST)
        if formSenha.is_valid():
            senhaAtual, novaSenha = formSenha.cleaned_data['senhaAtual'], formSenha.cleaned_data['novaSenha']
            user = Usuario.objects.get(cpf=cpf)
            if senhaAtual!=user.senha: return HttpResponse("Senha incorreta!")
            user.senha = novaSenha
            user.save()
            return render(request, 'mysite/configuracoes.html',d)

        formEmail = EmailForm(request.POST)
        if formEmail.is_valid():
            email = formEmail.cleaned_data['email']
            user = Usuario.objects.get(cpf=cpf)
            user.email = email
            user.save()
            return render(request, 'mysite/configuracoes.html',d)

        formDel = DeletaForm(request.POST)
        if formDel.is_valid():
            senha = formDel.cleaned_data['senha']
            user = Usuario.objects.get(cpf=cpf)
            if senha!=user.senha: return HttpResponse("Senha incorreta!")
            logout(request)
            user.delete()
            return redirect('cadastrar_usuario')


    return render(request, 'mysite/configuracoes.html',d)


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
        form = ConfirmacaoCancelamentoForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirmar']:
            carona.delete()
            return redirect('visualizar_caronas')
    else:
            form = ConfirmacaoCancelamentoForm()


    return render(request, 'mysite/cancelar_carona.html', {'carona': carona, 'form':form})
