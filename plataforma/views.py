from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from .models import Paciente, DadosPaciente, Refeicao, Opcao
from .utils import Verify
from datetime import datetime

# Create your views here.

@login_required(login_url='/auth/login')
def pacientes(request):
    match request.method:
        case "GET":
            patients = Paciente.objects.filter(nutri = request.user)

            return render(request, 'pacientes.html', {'pacientes': patients})

        case "POST":
            name = request.POST.get('nome')
            sex = request.POST.get('sexo')
            age = request.POST.get('idade')
            email = request.POST.get('email')
            phone = request.POST.get('telefone')

            if Verify.blank_inputs(request, name, sex, age, email, phone):
                return redirect('/pacientes')

            if not age.isnumeric():
                messages.add_message(request, constants.WARNING, "Digite uma idade válida!")
                return redirect('/pacientes')

            if not Verify.phone_number(request, phone):
                return redirect('/pacientes')

            pacient = Paciente.objects.filter(email = email)
            nutritionist = User.objects.filter(email = email)

            if pacient.exists():
                messages.add_message(request, constants.WARNING, "Já existe um paciente com esse e-mail!")
                return redirect('/pacientes')

            if nutritionist.exists():
                messages.add_message(request, constants.WARNING, "Já existe um(a) nutricionista com esse e-mail!")
                return redirect('/pacientes')

            try:
                pacient = Paciente(
                    nome = name,
                    sexo = sex,
                    idade = age,
                    email = email,
                    telefone = phone,
                    nutri = request.user
                )

                pacient.save()
                messages.add_message(request, constants.SUCCESS, "Paciente cadastrado com sucesso!")

                return redirect('/pacientes')

            except:
                messages.add_message(request, constants.ERROR, "Erro de sistema. Não foi possível cadastrar o paciente.")

                return redirect('/pacientes')

@login_required(login_url='/auth/login')
def dados_paciente(request):
    match request.method:
        case "GET":
            patients = Paciente.objects.filter(nutri = request.user)

            return render(request, 'dados_paciente.html', {'pacientes': patients})

@login_required(login_url='/auth/login')
def dados(request, id):
    patient = get_object_or_404(Paciente, id = id)
    if not patient.nutri == request.user:
        messages.add_message(request, constants.WARNING, "Esse paciente não é seu!")
        return redirect('/pacientes/dados')

    match request.method:
        case "GET":
            dados = DadosPaciente.objects.filter(paciente = patient)

            return render(request, 'dados.html', {'paciente': patient, 'dados': dados})

        case "POST":
            weight = request.POST.get('peso')
            height = request.POST.get('altura')
            fat_perc = request.POST.get('gordura')
            muscle_perc = request.POST.get('musculo')
            hdl = request.POST.get('hdl')
            ldl = request.POST.get('ldl')
            total_cholest = request.POST.get('ctotal')
            triglyc = request.POST.get('triglicerídios')

            if Verify.blank_inputs(request, 
                                    weight, 
                                    height, 
                                    fat_perc, 
                                    muscle_perc, 
                                    hdl, 
                                    ldl, 
                                    total_cholest, 
                                    triglyc):

                return redirect('/pacientes/dados')

            if not Verify.is_numeric(request, 
                                    weight, 
                                    height, 
                                    fat_perc, 
                                    muscle_perc, 
                                    hdl, 
                                    ldl, 
                                    total_cholest, 
                                    triglyc):

                return redirect('/pacientes/dados')

            patient = DadosPaciente(paciente = patient,
                                    data = datetime.now(),
                                    peso = weight,
                                    altura = height,
                                    percentual_gordura = fat_perc,
                                    percentual_musculo = muscle_perc,
                                    colesterol_hdl = hdl,
                                    colesterol_ldl = ldl,
                                    colesterol_total = total_cholest,
                                    trigliceridios = triglyc)

            patient.save()
            messages.add_message(request, constants.SUCCESS, "Dados cadastrados com sucesso!")

            return redirect('/pacientes/dados')

@login_required(login_url='/auth/login')
@csrf_exempt
def grafico(request, id):
    patient = Paciente.objects.get(id = id)
    data = DadosPaciente.objects.filter(paciente = patient).order_by('data')

    weights = [d.peso for d in data]
    labels = list(range(len(weights)))

    response = {'pesos': weights,
                'labels': labels}

    return JsonResponse(response)

@login_required(login_url='/auth/login')
def lista_plano_alimentar(request):
    match request.method:
        case "GET":
            pacientes = Paciente.objects.filter(nutri=request.user)
            return render(request, 'lista_plano_alimentar.html', {"pacientes": pacientes})

@login_required(login_url='/auth/login')
def plano_alimentar(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if paciente.nutri != request.user:
        messages.add_message(request, constants.WARNING, "Esse paciente não é seu!")
        return redirect('/pacientes/plano_alimentar')

    match request.method:
        case "GET":
            paciente = Paciente.objects.get(id=id)
            refeicoes = Refeicao.objects.filter(paciente=paciente).order_by('horario')
            opcoes = Opcao.objects.all()

            return render(request, 'plano_alimentar.html', {"paciente": paciente, "refeicoes": refeicoes, "opcoes": opcoes})

@login_required(login_url='/auth/login')
def refeicao(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if paciente.nutri != request.user:
        messages.add_messages(request, constants.WARNING, "Esse paciente não é seu!")
        return redirect('/pacientes/dados')

    match request.method:
        case "GET":
            raise Http404()

        case "POST":
            titulo = request.POST.get('titulo')
            horario = request.POST.get('horario')
            carboidratos = request.POST.get('carboidratos')
            proteinas =  request.POST.get('proteinas')
            gorduras = request.POST.get('gorduras')

            if Verify.blank_inputs(request, titulo, horario, carboidratos, proteinas, gorduras):
                return redirect(f'/pacientes/plano_alimentar/{id}')

            try:
                paciente = Paciente.objects.get(id=id)

                refeicao = Refeicao(paciente=paciente,
                                    titulo=titulo,
                                    horario=horario,
                                    carboidratos=carboidratos,
                                    proteinas=proteinas,
                                    gorduras=gorduras)

                refeicao.save()
                messages.add_message(request, constants.SUCCESS, "Refeição cadastrada com sucesso!")
                return redirect(f'/pacientes/plano_alimentar/{id}')

            except:
                messages.add_message(request, constants.ERROR, "Erro interno do sistema. Não foi possível cadastrar a refeição.")
                return redirect(f'/pacientes/plano_alimentar/{id}')

@login_required(login_url='/auth/login')
def opcao(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.WARNING, "Esse paciente não é seu!")
        return redirect('/pacientes/plano_alimentar')

    match request.method:
        case "GET":
            raise Http404()

        case "POST":
            id_refeicao = request.POST.get('refeicao')
            imagem = request.FILES.get('imagem')
            descricao = request.POST.get('descricao')
            
            try:
                paciente = Paciente.objects.get(id=id)
                refeicao = Refeicao.objects.get(id=id_refeicao)

                opcao = Opcao(refeicao=refeicao,
                            imagem=imagem,
                            descricao=descricao)

                opcao.save()
                messages.add_message(request, constants.SUCCESS, f"Opção de {refeicao.titulo} cadastrada com sucesso.")
                return redirect(f'/pacientes/plano_alimentar/{id}')

            except:
                messages.add_message(request, constants.SUCCESS, f"Erro interno do sistema. Não foi possível cadastrar a opção.")
                return redirect(f'/pacientes/plano_alimentar/{id}')
