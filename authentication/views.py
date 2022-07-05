from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .utils import Verify, Send
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.conf import settings
from .models import Ativacao, Recuperacao
from hashlib import sha256

# Create your views here.
def register(request):
    match request.method:
        case "GET":
            if request.user.is_authenticated:
                return redirect('/')

            return render(request, 'register.html')

        case "POST":
            username = request.POST.get("usuario")
            email = request.POST.get("email")
            password = request.POST.get("senha")
            confirm_password = request.POST.get("confirmar_senha")

            if not Verify.password_is_valid(request, password, confirm_password):
                return redirect('/auth/register')

            try:
                _username = User.objects.filter(username = username)
                
                if _username:
                    messages.add_message(request, constants.WARNING, f"Usuário de nome {username} já existe! Tente outro.")
                    return redirect('/auth/register')

                _email = User.objects.filter(email__exact = email)

                if _email:
                    messages.add_message(request, constants.WARNING, f"Usuário de email {email} já existe! Tente outro.")
                    return redirect('/auth/register')

                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                    is_active = False
                )

                user.save()

                token = sha256(f"{username}{email}".encode()).hexdigest()
                activation = Ativacao(
                    token = token,
                    user = user
                )

                activation.save()

                Send.email(
                    settings.ACTIVATION_PATH_TEMPLATE, "Cadastro confirmado",
                    [email],
                    username = username,
                    link_ativacao = f"127.0.0.1:8000/auth/activate/{token}")

                messages.add_message(request, constants.SUCCESS, "Usuário cadastrado com sucesso!")
                return redirect('/auth/login')

            except:
                messages.add_message(request, constants.ERROR, "Erro de sistema. Tente novamente mais tarde.")
                return redirect('/auth/register')

def login(request):
    match request.method:
        case "GET":
            if request.user.is_authenticated:
                return redirect('/')

            return render(request, 'login.html')

        case "POST":
            username = request.POST.get('usuario')
            password = request.POST.get('senha')

            user = auth.authenticate(username = username, password = password)

            if not user:
                messages.add_message(request, constants.ERROR, "Usuário passado não existe! Verifique seu usuário ou senha.")
                return redirect('/auth/login')

            else:
                auth.login(request, user)
                return redirect('/')

def logout(request):
    auth.logout(request)
    return redirect('/auth/login')

def activate_account(request, token):
    token = get_object_or_404(Ativacao, token = token)
    if token.ativo:
        messages.add_message(request, constants.WARNING, "Esse token já foi usado.")
        return redirect('/auth/login')

    user = User.objects.get(username = token.user.username)
    user.is_active = True
    user.save()
    
    token.ativo = True
    token.save()

    messages.add_message(request, constants.SUCCESS, "Conta ativada com sucesso!")
    return redirect('/auth/login')

def recover_password_email(request):
    match request.method:
        case "GET":
            if request.user.is_authenticated:
                return redirect('/')

            return render(request, 'recover_menu.html')

        case "POST":
            username = request.POST.get("usuario")
            email = request.POST.get("email")

            _user = User.objects.filter(username = username, email = email)
            if _user:
                user = User.objects.get(username = username)
                _token = Recuperacao.objects.filter(user = user)
                token = sha256(f"{username}{email}".encode()).hexdigest()

                if not _token:
                    user_token = Recuperacao(
                        token = token,
                        user = user
                    )

                    user_token.save()

                    Send.email(
                        settings.RECOVER_PATH_TEMPLATE,
                        "Alterar Senha",
                        [email],
                        username = username,
                        link_recuperacao = f"127.0.0.1:8000/auth/recover/{token}",
                        link_seguranca = f"127.0.0.1:8000/auth/norecover/{token}"
                    )

                    messages.add_message(request, constants.SUCCESS, f"E-mail de recuperação enviado com sucesso para {email}")

                    return redirect('/auth/login')
                
                else:
                    user_token = Recuperacao.objects.get(user = user)
                    user_token.token = token
                    user_token.ativo = True

                    user_token.save()

                    Send.email(
                        settings.RECOVER_PATH_TEMPLATE,
                        "Alterar Senha",
                        [email],
                        username = username,
                        link_recuperacao = f"127.0.0.1:8000/auth/recover/{token}",
                        link_seguranca = f"127.0.0.1:8000/auth/norecover/{token}"
                    )

                    messages.add_message(request, constants.SUCCESS, f"E-mail de recuperação enviado com sucesso para {email}")

                    return redirect('/auth/login')

            if not _user:
                messages.add_message(request, constants.ERROR, "Esse usuário não existe!")
                return redirect('/auth/recover')

def recover_password(request, token):
    match request.method:
        case "GET":
            _token = get_object_or_404(Recuperacao, token = token)
            if not _token.ativo:
                return redirect('/auth/login')

            return render(request, 'recover_password.html', {"token": token})

        case "POST":
            _token = get_object_or_404(Recuperacao, token = token)
            new_password = request.POST.get('nova_senha')
            confirm_password = request.POST.get('confirmar_senha')

            if not _token.ativo:
                messages.add_message(request, constants.WARNING, "Não houve nenhuma solicitação de recuperação de senha.")
                return redirect('/auth/login')

            if new_password != confirm_password:
                messages.add_message(request, constants.WARNING, "As senhas não coincidem.")
                return redirect(f'/auth/recover/{token}')

            else:
                user = User.objects.get(username = _token.user.username)
                user.set_password(new_password)
                user.save()

                _token.ativo = False
                _token.save()

                messages.add_message(request, constants.SUCCESS, "Senha alterada com sucesso!")
                return redirect('/auth/login')

def norecover_password(request, token):
    _token = get_object_or_404(Recuperacao, token = token)
    if not _token.ativo:
        return redirect('/auth/login')

    _token.ativo = False
    _token.save()

    messages.add_message(request, constants.WARNING, "Pedido de alteração de senha recusado com sucesso!")
    return redirect('/auth/login')
