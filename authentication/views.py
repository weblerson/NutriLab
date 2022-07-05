from django.shortcuts import render, redirect, get_object_or_404
from .utils import Verify, Send
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.messages import constants
from django.conf import settings
from .models import Ativacao
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
                    settings.PATH_TEMPLATE, "Cadastro confirmado",
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
    if request.user.is_authenticated:
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