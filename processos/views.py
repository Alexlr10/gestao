import decimal
from time import strptime

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datetime_safe import strftime, datetime
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail, send_mass_mail
from .forms import *
from .models import *
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json




class usuariosUpdate(UpdateView):
    model = Usuario
    fields = ('Nome',
              'Login',
              'Situacao',
              'CPF',
              'Email',
              'Funcao',
              )
    success_url = reverse_lazy('usuarios')
    template_name = 'usuario_edit.html'


class usuariosDelete(DeleteView):
    model = Usuario
    success_url = reverse_lazy('usuarios')
    template_name = 'usuarios_delete.html'

@login_required
def usuario_edit(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioCreationForm(request.POST or None, instance=usuario)

    if form.is_valid():
        form.save()

        send_mail(
            'NextStep - Atualização',
            'Suas informações de perfil foram atualizadas',
            'alexlr10.al@gmail.com',
            [usuario.Email],
            fail_silently=False,
        )
        return redirect('usuarios')

    context = {
        'form': form,
        'usuario': usuario
    }

    return render(request, 'usuario_edit.html', context)

@login_required
def usuario_delete(request, pk):
    usuario = Usuario.objects.get(pk=pk)
    usuario.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('usuarios')


def usuarios(request):
    if request.POST:
        usuario = Usuario.objects.all()
        form = UsuarioCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('usuarios')
        context = {
            'usuario': usuario,
            'form': form
        }

        return render(request, 'usuarios.html', context)

    form = UsuarioCreationForm()

    usuario = Usuario.objects.all().order_by('-id')[:100]  # ORM do Django

    ultima_imp = Usuario.objects.all().order_by('-id')[:1]

    context = {
        'usuario': usuario,
        'form': form,
        'ultima_imp': ultima_imp
        # 'Filial': i,

    }

    return render(request, 'usuarios.html', context)


@login_required
def editar_meus_dados(request):
    if request.method == 'POST' and request.POST.get('usuarioSenha') != None:
        usuario = get_object_or_404(Usuario, pk=request.user.id)

        usuario.Nome = request.POST.get('nomeUsuario')
        usuario.Email = request.POST.get('emailUsuario')
        usuario.Celular = request.POST.get('celularUsuario')
        usuario.CPF = request.POST.get('cpfUsuario')
        usuario.RG = request.POST.get('rgUsuario')
        usuario.set_password(request.POST.get('usuarioSenha'))
        usuario.save()

        send_mail(
            'NextStep - Atualização',
            'Você atualizou as informações do seu perfil',
            'sistemanextstepsi@gmail.com',
             [usuario.Email],
            fail_silently=False,
        )
        messages.success(request, 'Dados alterados com sucesso')

        return redirect(reverse('meusdados'))

    usuario = request.user
    context = {
        'usuario': usuario
    }

    return render(request, 'meus_dados.html', context)



def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError



# @login_required
# def home(request):
#     ouvidoria = Ouvidoria.objects.all()
#
#
#     context = {
#        'ouvidoria':ouvidoria
#     }
#     return render(request,'home.html',context)

@login_required
def home(request):
    ouvidoria = Ouvidoria.objects.all()
    if request.method == 'POST':
        form = OuvidoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Menssagem enviada com sucesso')
            return redirect('home')

    form = OuvidoriaForm()

    context = {
        'form': form,
        'ouvidoria': ouvidoria
    }

    return render(request,'home.html',context)

@login_required
def contas(request):

    return render(request, 'contas.html')

@login_required
def mensagem(request):
    ouvidoria = Ouvidoria.objects.all()

    form = OuvidoriaForm()

    context = {
        'form': form,
        'ouvidoria': ouvidoria
    }

    return render(request,'mensagens.html',context)

@login_required
def ouvidoria(request):
    ouvidoria = Ouvidoria.objects.all()
    if request.method == 'POST':
        form = OuvidoriaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Menssagem enviada com sucesso')
            return redirect('ouvidoria')

    form = OuvidoriaForm()

    context = {
        'form': form,
        'ouvidoria': ouvidoria
    }

    return render(request,'ouvidoria.html',context)

def grafico(request):
    balanco = Balanco.objects.raw('''SELECT DISTINCT  1 as id,to_char(processos_balanco."datas", 'MM-YYYY') as periodo,
                                       sum(receita) as rendimento,  sum(despesa) as despesa,
                                         (sum(receita) - sum(despesa)) as total FROM 
                                           public.processos_balanco GROUP BY to_char(processos_balanco."datas", 'MM-YYYY')''')


    total = [obj.total for obj in balanco]

    datas = [obj.periodo for obj in balanco]
    datas.sort()
    balancos = [obj.total for obj in balanco]

    rendimentos = [obj.rendimento for obj in balanco]

    context = {
        'total': json.dumps(total, default=decimal_default),

        'datas': json.dumps(datas),
        'balancos': json.dumps(balancos, default=decimal_default),

        'rendimentos': json.dumps(rendimentos, default=decimal_default),

    }


    return render(request, 'graficos.html', context)

######## Cliente
@login_required
def cliente(request):
    cliente = Cliente.objects.all()
    if request.method == 'POST':
        form = ClienteForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso')
            return redirect('cliente')

    form = ClienteForm()

    context = {
        'form': form,
        'cliente': cliente
    }

    return render(request, 'cliente.html', context)


@login_required
def cliente_edit(request, pk):
    cliente = Cliente.objects.get(pk=pk)

    form = ClienteForm(request.POST or None, instance=cliente)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cadastro alterado com sucesso')
        return redirect('cliente')

    context = {
        'form': form,
        'cliente': cliente
    }

    return render(request, 'cliente_edit.html', context)

@login_required
def cliente_delete(request, pk):
    cliente = Cliente.objects.get(pk=pk)
    cliente.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('cliente')



######## Serviço
@login_required
def servico(request):
    servico = Servico.objects.all()
    if request.method == 'POST':
        form = ServicoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço cadastrado com sucesso')
            return redirect('servico')

    form = ServicoForm()

    context = {
        'form': form,
        'servico': servico
    }

    return render(request, 'servico.html', context)

@login_required
def servico_edit(request, pk):
    servico = Servico.objects.get(pk=pk)

    form = ServicoForm(request.POST or None, instance=servico)

    if form.is_valid():
        form.save()
        messages.success(request, 'Cadastro alterado com sucesso')
        return redirect('servico')

    context = {
        'form': form,
        'servico': servico
    }

    return render(request, 'servico_edit.html', context)

@login_required
def servico_delete(request, pk):
    servico = get_object_or_404(Servico,pk=pk)
    servico.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('servico')




######## Projeto
@login_required
def projeto(request):
    projeto = Projeto.objects.all()
    if request.method == 'POST':
        form = ProjetoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto cadastrado com sucesso')
            return redirect('projeto')

    form = ProjetoForm()

    context = {
        'form': form,
        'projeto': projeto
    }

    return render(request, 'projeto.html', context)

@login_required
def projeto_edit(request, pk):
    projeto = get_object_or_404(Projeto, pk=pk)

    form = ProjetoForm(request.POST or None, instance=projeto)

    if form.is_valid():
        form.save()
        return redirect('projeto')

    context = {
        'form': form,
        'projeto': projeto
    }

    return render(request, 'projeto_edit.html', context)

@login_required
def projeto_delete(request, pk):
    projeto = get_object_or_404(Projeto,pk=pk)
    projeto.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('projeto')


######## Reuniao
@login_required
def reuniao(request):
    reuniao = Reuniao.objects.all()
    if request.method == 'POST':
        form = ReuniaoForm(request.POST)

        if form.is_valid():
            form.save()
            dataReuniao = request.POST.get('dataReuniao')
            tipoReuniao = request.POST.get('tipoReuniao')
            data = dataReuniao.split('-')
            pauta = request.POST.get('descricaoReuniao')

            if tipoReuniao == 'GER':
                mensagem = str('A Next terá uma reunião GERAL dia '+ data[2] + ' do '+  data[1] + ' com as seguintes paltas: \n' + pauta)
            elif tipoReuniao == 'DIR':
                mensagem = str('A Next terá uma reunião de DIRETORIA dia '+ data[2] + ' do '+  data[1] + ' com as seguintes paltas: \n' + pauta)
            elif tipoReuniao == 'PRO':
                mensagem = str('A Next terá uma reunião da equipe de PROJETOS dia '+ data[2] + ' do '+  data[1] + ' com as seguintes paltas: \n' + pauta)


            reu = Reuniao.objects.last()
            membros = str(reu)
            email = membros.split(',')
            print(email)

            send_mail(
                'NextStep - REUNIÃO',
                 mensagem,
                'sistemanextstepsi@gmail.com',
                 email,
                fail_silently=False,
            )


            messages.success(request, 'Reunião cadastrada com sucesso')
            return redirect('reuniao')

    form = ReuniaoForm()

    context = {
        'form': form,
        'reuniao': reuniao
    }

    return render(request, 'reuniao.html', context)

@login_required
def reuniao_edit(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)

    form = ReuniaoForm(request.POST or None, instance=reuniao)

    if form.is_valid():
        form.save()
        return redirect('reuniao')

    context = {
        'form': form,
        'reuniao': reuniao
    }

    return render(request, 'reuniao_edit.html', context)

@login_required
def reuniao_delete(request, pk):
    reuniao = get_object_or_404(Reuniao,pk=pk)
    reuniao.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('reuniao')


######## Ata
@login_required
def ata(request):
    ata = Ata.objects.all()
    if request.method == 'POST':
        form = AtaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Ata cadastrada com sucesso')
            return redirect('ata')

    form = AtaForm()

    context = {
        'form': form,
        'ata': ata
    }

    return render(request, 'ata.html', context)

@login_required
def ata_edit(request, pk):
    ata = get_object_or_404(Ata, pk=pk)

    form = AtaForm(request.POST or None, instance=ata)

    if form.is_valid():
        form.save()
        return redirect('ata')

    context = {
        'form': form,
        'ata': ata
    }

    return render(request, 'ata_edit.html', context)

@login_required
def ata_delete(request, pk):
    ata = get_object_or_404(Ata,pk=pk)
    ata.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('ata')


######## Receitas
@login_required
def receita(request):
    receita = Receita.objects.all()

    if request.method == 'POST':
        form = ReceitaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Receita cadastrada com sucesso')
            return redirect('receita')

    form = ReceitaForm()

    context = {
        'form': form,
        'receita': receita
    }

    return render(request, 'receita.html', context)

@login_required
def receita_edit(request, pk):
    receita = get_object_or_404(Receita, pk=pk)
    balanco = Balanco.objects.get(receitas_id=pk)
    form = ReceitaForm(request.POST or None, instance=receita)

    if form.is_valid():
        balanco.delete()
        form.save()
        return redirect('receita')

    context = {
        'form': form,
        'receita': receita
    }

    return render(request, 'receita_edit.html', context)

@login_required
def receita_delete(request, pk):
    receita = get_object_or_404(Receita,pk=pk)
    receita.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('receita')


@login_required
def despesa(request):
    despesa = Despesas.objects.all()
    form = DespesasForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('despesa')

    context = {

        'form': form,
        'despesa':despesa
    }

    return render(request, 'despesa.html', context)

@login_required
def despesa_delete(request,pk):
    despesa = get_object_or_404(Despesas,pk=pk)
    despesa.delete()
    return redirect('despesa')

@login_required
def despesa_edit(request, pk):

    despesa = get_object_or_404(Despesas, pk=pk)
    balanco = Balanco.objects.get(despesa_id=pk)
    form = DespesasForm(request.POST or None, instance=despesa)

    if form.is_valid():
        balanco.delete()
        form.save()
        return redirect('despesa')

    context = {
        'form': form,
        'despesa': despesa
    }

    return render(request, 'despesa_edit.html', context)

@login_required
def balanco(request):
    balanco = Balanco.objects.raw('''SELECT DISTINCT  1 as id,to_char(processos_balanco."datas", 'MM-YYYY') as periodo,
                                    sum(receita) as rendimento,  sum(despesa) as despesa,
                                      (sum(receita) - sum(despesa)) as total FROM 
                                        public.processos_balanco GROUP BY to_char(processos_balanco."datas", 'MM-YYYY')''')

    balancoCompleto = Balanco.objects.all().order_by('-datas')
    form = BalancoForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('balanco')

    context = {

        'form': form,
        'balanco': balanco,
        'balancoCompleto':balancoCompleto,

    }

    return render(request, 'balanco.html', context)

@login_required
def balanco_delete(request,pk):
    balanco = get_object_or_404(Balanco,pk=pk)
    balanco.delete()
    return redirect('balanco')

@login_required
def balanco_edit(request, pk):

    balanco = get_object_or_404(Balanco, pk=pk)

    form = BalancoForm(request.POST or None, instance=balanco)

    if form.is_valid():
        form.save()
        return redirect('balanco')

    context = {
        'form': form,
        'balanco': balanco
    }

    return render(request, 'balanco_edit.html', context)

@login_required
def historico_membros(request):
    historico = HistoricoMembros.objects.all()

    form = HistoricoForm()
    context = {
        'historico': historico,
        'form': form
    }

    return render(request, 'historicoMembros.html', context)