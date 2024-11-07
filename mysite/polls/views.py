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
            request.session['data_nascimento'] = form.cleaned_data['data_nascimento'].isoformat()
            request.session['telefone'] = form.cleaned_data['telefone']

            if e_motorista:
                return JsonResponse({'success': True, 'redirect': 'veiculo'})

            usuario = Usuario(
                cpf=request.session['cpf'],
                email=request.session['email'],
                nome=request.session['nome'],
                senha=request.session['senha'],
                data_nascimento=datetime.fromisoformat(request.session['data_nascimento']).date(),
                telefone=request.session['telefone'],
            )
            usuario.save()
            
            # Remover dados de sessão para segurança
            del request.session['email']
            del request.session['senha']
            del request.session['data_nascimento']
            del request.session['telefone']
            
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
    d = {
         'formnome'     : NomeForm(),
         'formdata'     : DataForm(),
         'formtel'      : TelefoneForm(),
         'formsen'      : SenhaForm(),
         'formemail'    : EmailForm(),
         'formdel'      : DeletaForm(),
         'eh_motorista'   : motorista,
         'nome'           : usuario.nome,
         'data'           : usuario.data_nascimento,
         'tel'            : usuario.telefone,
         'email'          : usuario.email
        }

    
    if request.method == 'POST':
        formNome = NomeForm(request.POST)
        formData = DataForm(request.POST)
        formTel = TelefoneForm(request.POST)

        # if 'cadastra' in request.POST: return redirect('veiculo')
        
        # if 'descadastra_veiculo' in request.POST:
        #     Veiculo.objects.filter(cpf_motorista = cpf).delete()
        #     return HttpResponse('Veĩculo descadastrado com sucesso')

        if formNome.has_changed() and formNome.is_valid():
            novoNome = formNome.cleaned_data['nome']
            usuario.nome = novoNome
            usuario.save()
            return HttpResponse("Nome alterado com sucesso")

        if formData.has_changed():
            if formData.is_valid():
                novaData = formData.cleaned_data['data']
                usuario.data_nascimento = novaData
                usuario.save()
                return HttpResponse('Data de nascimento alterada com sucesso')
            else: 
                print('teste2')
                return HttpResponse("Você deve ter ao menos 13 anos para utilizar o sistema")
        
        if formTel.has_changed() :
            if formTel.is_valid():
                alterou = True
                novoTel = formTel.cleaned_data['telefone']
                usuario.telefone = novoTel
                usuario.save()
                return HttpResponse('Telefone alterado com sucesso')

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
            return HttpResponse('Sua conta foi excluída com sucesso')

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
        carona.delete()
        return redirect('visualizar_caronas')

def listar_caronas(request):
    destino = request.GET.get('Destino')
    data = request.GET.get('data')
    caronas =  Carona.objects.none()
    consultado = False
    
    print("Destino: ",destino)
    print("Data: ",data)
    
    
    if destino and data:
        try:
            consultado = True
            data_formatado = datetime.strptime(data, '%Y-%m-%d').date()
            caronas =  Carona.objects.all()
            caronas = caronas.filter(destino__iexact = destino, data_hora__date=data_formatado)
            print("caronas encontradas", caronas)
        except ValueError:
            pass
        

    return render(request, 'mysite/consulta.html', {'caronas':caronas, 'consultado': consultado})
