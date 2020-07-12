import decimal

from django.db.models import Sum, F, Q
from django.db.models.functions import TruncMonth, TruncYear
from django.shortcuts import render, redirect, get_object_or_404

from django.utils.datetime_safe import strftime, datetime
from django.utils.html import strip_tags
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail, send_mass_mail
from .forms import *
from .models import *
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json



def usuarios(request):
    if request.POST:
        usuario = Usuario.objects.all()
        form = UsuarioCreationForm(request.POST)

        if form.is_valid():
            form.save()
            #PEGANDO O LOGIN E O EMAIL CADASTRADO PARA ENVIAR A MENSAGEM POR EMAIL PARA O NOVO USUARIO
            login = request.POST.get('Login')
            email = request.POST.get('Email')
            mensagem = str('Parabens!!! Você agora é um novo membro Empresa Júnior Next Step!!\n'
                           'Login: '+ login + '\n Senha: 12345678\n'
                                              'você pode alterar à qualquer momento acessando '
                                              'seu Perfil-Meus Dados no sistema')
            #FUNCAO PARA ENVIO DE EMAIL
            send_mail(
                'Empresa Júnior Next Step Step',
                mensagem,
                'sistemanextstepsi@gmail.com',
                [email],
                fail_silently=False,
            )
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

    }

    return render(request, 'usuarios.html', context)


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
    messages.error(request, 'Usuarios removido com sucesso')

    return redirect('usuarios')

@login_required
def editar_meus_dados(request):
    if request.POST.get('password') != None:

        usuario = get_object_or_404(Usuario, pk=request.user.id)

        form = MeusDadosForm(request.POST or None, request.FILES or None, instance=usuario)
        print(form.errors)
        if form.is_valid():
            Email = request.POST.get('Email')
            form.save()
            send_mail(
                'NextStep - Atualização',
                'Você atualizou as informações do seu perfil',
                'sistemanextstepsi@gmail.com',
                 [Email],
                fail_silently=False,
            )
            messages.success(request, 'Dados alterados com sucesso')

            return redirect(reverse('meusdados'))

    usuario = request.user
    form = MeusDadosForm(request.POST or None, request.FILES or None, instance=usuario)
    context = {
        'form':form,
        'usuario': usuario
    }

    return render(request, 'meus_dados.html', context)




def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def date_handler(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat(obj)
    raise TypeError

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
def mensagem(request):
    ouvidoria = Ouvidoria.objects.all().order_by('-data')
    print(ouvidoria)

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
            #BUSCA O EMAIL DOS MEMBROS DO RH PARA AVISAR QUE A UMA MENSAGEM DA OUVIDORIA
            email = [u for u in Usuario.objects.values_list('Email', flat=True).filter(Funcao='RH').filter(Situacao = True)]
            print(email)
            mensagem = 'O RH acaba de receber uma mensagem via Ouvidoria Next Step, por favor verifique o sistema de Gestão Interna'
            send_mail(
                'Ouvidoria Next Step',
                mensagem,
                'sistemanextstepsi@gmail.com',
                email,
                fail_silently=False,
            )
            return redirect('ouvidoria')

    form = OuvidoriaForm()

    context = {
        'form': form,
        'ouvidoria': ouvidoria
    }

    return render(request,'ouvidoria.html',context)

@login_required
def aviso(request):
    aviso = Aviso.objects.all()
    usu = Usuario.objects.filter(Situacao=True).order_by('Nome')
    usuario = []
    for u in usu:
        usuario.append(u)

    if request.method == 'POST':
        form = AvisoForm(request.POST)

        if form.is_valid():
            form.save()
            #PEGANDO INFORMAÇOES DO FORMULARIO PARA ENVIO DO EMAIL
            Data = request.POST.get('Data')
            assunto = request.POST.get('assunto')
            descricao = request.POST.get('descricao')

            mensagem = strip_tags(descricao)

            #BUSCANDO DO BANCO OS ULTIMOS DADOS CADASTRADOS PARA ENVIO DO EMAIL
            aviso = Aviso.objects.last()
            membros = [u for u in aviso.membros.values_list('Email', flat=True)]
            email = membros
            print(email)

            send_mail(
                 assunto,
                 mensagem,
                'sistemanextstepsi@gmail.com',
                 email,
                fail_silently=False,
            )


            messages.success(request, 'Email enviado com sucesso aos membros')
            return redirect('aviso')

    form = AvisoForm()

    context = {
        'form': form,
        'aviso': aviso,
        'usuario':usuario
    }

    return render(request, 'aviso.html', context)

#FUNCAO PARA BUSCAR OS DADOS PARA PLOTAGEM DO GRAFICO
def grafico(request):
    balanco = Balanco.objects.raw('''SELECT DISTINCT  1 as id,to_date(to_char(processos_balanco."datas", 'MM-YYYY'), 'MM YYYY') as periodo,
                                       sum(receita) as rendimento,  sum(despesa) as despesa,
                                         (sum(receita) - sum(despesa)) as total FROM
                                           public.processos_balanco 
                                           WHERE processos_balanco."Pagamento" = true
                                           GROUP BY to_date(to_char(processos_balanco."datas", 'MM-YYYY'), 'MM YYYY')
                                           ORDER BY to_date(to_char(processos_balanco."datas", 'MM-YYYY'), 'MM YYYY')''')

    receitaAReceber = Receita.objects.raw('''SELECT 1 as id, to_char(processos_receita."Data", 'MM-YYYY') as periodo,
                                              Sum(processos_receita."valorParcela") as receita
                                              FROM   public.processos_receita
                                                WHERE processos_receita."Pagamento" = true
                                                 GROUP BY to_char(processos_receita."Data",'MM-YYYY')
                                                 ORDER BY to_date(to_char(processos_receita."Data", 'MM-YYYY'), 'MM YYYY')''')



    #TRANSFORMANDDO DATA EM STRING E CONCATENANDO A ORDEM DE EXIBIÇAO
    datas = [str (obj.periodo)[5:7] + '-' + str (obj.periodo)[0:4] for obj in balanco]

    balancos = [obj.total for obj in balanco]

    rendimentos = [obj.rendimento for obj in balanco]

    receita = [obj.receita for obj in receitaAReceber]
    data = [str (obj.periodo) for obj in receitaAReceber]

    print(datas)

    #UTILIZANDO FUNCAO JSON,DUMPS PARA TRANSFORMAR OS DADOS EM JSON
    context = {

        'datas': json.dumps(datas),
        'balancos': json.dumps(balancos, default=decimal_default),

        'rendimentos': json.dumps(rendimentos, default=decimal_default),

        'receita': json.dumps(receita, default=decimal_default),
        'data': json.dumps(data)
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
        'projeto': projeto,
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
        'projeto': projeto,
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
    reuniao = Reuniao.objects.all().order_by('-dataReuniao')


    if request.method == 'POST':
        form = ReuniaoForm(request.POST)
        #PEGANDO AS INFORMAÇOES DO FORMULARIO PARA ENVIO DO EMAIL
        if form.is_valid():
            form.save()
            dataReuniao = request.POST.get('dataReuniao')
            tipoReuniao = request.POST.get('tipoReuniao')
            data = dataReuniao.split('-')
            pauta = request.POST.get('descricaoReuniao')

            #VERIFICANDO QUAL FOI O TIPO DE REUNIAO CADASTRADA
            if tipoReuniao == 'GERAL':
                mensagem = str('A Next Step marca uma reunião GERAL no dia '+ data[2] + '/'+  data[1] +'/'+  data[0] + ', com as seguintes instruções: \n' + pauta)
            elif tipoReuniao == 'DIRETORIA':
                mensagem = str('A Next Step marca uma reunião DIRETORIA no dia '+ data[2] + '/'+  data[1] +'/'+  data[0] + ', com as seguintes instruções: \n' + pauta)
            elif tipoReuniao == 'PROJETOS':
                mensagem = str('A Next Step marca uma reunião PROJETOS no dia '+ data[2] + '/'+  data[1] +'/'+  data[0] + ', com as seguintes instruções: \n' + pauta)
            elif tipoReuniao == 'EXTERNA':
                mensagem = str('A Next Step marca uma reunião EXTERNA no dia '+ data[2] + '/'+  data[1] +'/'+  data[0] + ', com as seguintes instruções: \n' + pauta)


            #BUSCANDO A ULTIMA REUNIAO CADASTRADA PARA O ENVIO DO EMAIL
            reu = Reuniao.objects.last()
            email = [u for u in reu.presenca.values_list('Email', flat=True)]#FLAT=TRUE NAO EXIBE A CHAVE NA LISTA

            print(email)

            send_mail(
                'Empresa Júnior Next Step - REUNIÃO',
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
        'reuniao': reuniao,
    }

    return render(request, 'reuniao.html', context)

@login_required
def reuniao_edit(request, pk):
    reuniao = get_object_or_404(Reuniao, pk=pk)


    form = ReuniaoForm(request.POST or None, instance=reuniao)

    if form.is_valid():
        form.save()
        # BUSCANDO A ULTIMA REUNIAO CADASTRADA PARA O ENVIO DO EMAIL
        reu = Reuniao.objects.last()
        email = [u for u in reu.presenca.values_list('Email', flat=True)]#FLAT=TRUE NAO EXIBE A CHAVE NA LISTA
        print(email)
        mensagem = str('Caro membro, você faltou na reunião '
                       '' + reu.tipoReuniao + ' da data de ' + str(
            reu.dataReuniao.strftime("%d/%m/%Y")) + ' e não foi justificada,'
                                                    ' sua falta será contabilizada em nosso sistema.'
                                                    'Em caso de dúvidas entre em contato com o RH.')
        send_mail(
            'NextStep - REUNIÃO',
            mensagem,
            'sistemanextstepsi@gmail.com',
            email,
            fail_silently=False,
        )
        return redirect('reuniao')


    context = {
        'form': form,
        'reuniao': reuniao,

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
    ata = Ata.objects.all().order_by('-dataPublicacao')
    if request.method == 'POST':
        #REQUEST FILE USADO PARA ARQUIVO OU IMAGEM
        form = AtaForm(request.POST, request.FILES)

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

    form = AtaForm(request.POST or None, request.FILES or None, instance=ata)

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
    receita = Receita.objects.all().order_by('-Data')
    # receitaAReceber = Receita.objects.raw('''SELECT 1 as id, to_date(to_char(processos_receita."Data", 'MM-YYYY'), 'MM-YYYY') as periodo,
    #                                           Sum(processos_receita."valorParcela") as receita
    #                                           FROM   public.processos_receita
    #                                             WHERE processos_receita."Pagamento" = false
    #                                              GROUP BY to_char(processos_receita."Data",'MM-YYYY')
    #                                              ORDER BY to_char(processos_receita."Data",'MM-YYYY') ''')



    receitaAReceber = Receita.objects.filter(Pagamento=False).values(mes=TruncMonth('Data')).annotate(receita=Sum('valorParcela')).order_by('-mes')


    if request.method == 'POST':
        form = ReceitaForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Receita cadastrada com sucesso')
            return redirect('receita')

    form = ReceitaForm()

    context = {
        'form': form,
        'receita': receita,
        'receitaAReceber':receitaAReceber,
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
    balanco = Balanco.objects.get(receitas_id=pk)
    balanco.delete()
    receita.delete()
    messages.error(request, 'Cadastro removido com sucesso')

    return redirect('receita')


@login_required
def despesa(request):
    despesa = Despesas.objects.all().order_by('-data')
    despesaaPagar = Despesas.objects.filter(Pagamento=False).order_by('-data')
    today = datetime.today()

    form = DespesasForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registrado com sucesso')
            return redirect('despesa')

    context = {

        'form': form,
        'despesa':despesa,
        'despesaaPagar':despesaaPagar,
        'today':today
    }

    return render(request, 'despesa.html', context)

@login_required
def despesa_delete(request,pk):
    despesa = get_object_or_404(Despesas,pk=pk)
    balanco = Balanco.objects.get(despesa_id=pk)
    balanco.delete()
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
    # balanco = Balanco.objects.raw('''SELECT DISTINCT  1 as id,to_date(to_char(processos_balanco."datas", 'MM-YYYY'), 'MM YYYY') as periodo,
    #                                    sum(receita) as rendimento,  sum(despesa) as despesa,
    #                                      (sum(receita) - sum(despesa)) as total FROM
    #                                        public.processos_balanco
    #                                        WHERE processos_balanco."Pagamento" = true
    #                                        GROUP BY to_date(to_char(processos_balanco."datas", 'MM-YYYY'), 'MM YYYY')
    #                                        ORDER BY to_date(to_char(processos_balanco."datas", 'MM-YYYY'), 'MM YYYY') DESC''')


    balanco = Balanco.objects.filter(Pagamento=True).\
        values(mes=TruncMonth('datas')).\
        annotate(receita=Sum('receita'),despesa=Sum('despesa'),total=F("receita") - F("despesa")).order_by('-mes')



    # balancoPrimeiroSemestre = Balanco.objects.raw('''SELECT DISTINCT 1 as id,to_char(processos_balanco."datas", 'YYYY') as ano,
    #                                                 sum(receita) as rendimento,
    #                                                 sum(despesa) as despesa, (sum(receita) - sum(despesa)) as total
    #                                                 FROM public.processos_balanco  where
    #                                                 processos_balanco."Pagamento" = true and
    #                                                 (to_char(processos_balanco."datas", 'MM') = '01'
    #                                                 or to_char(processos_balanco."datas", 'MM') = '02' or
    #                                                 to_char(processos_balanco."datas", 'MM') = '03' or
    #                                                  to_char(processos_balanco."datas", 'MM') = '04' or
    #                                                  to_char(processos_balanco."datas", 'MM') = '05' or
    #                                                  to_char(processos_balanco."datas", 'MM') = '06')
    #                                                   GROUP BY to_char(processos_balanco."datas", 'YYYY') ''')
    #

    balancoPrimeiroSemestre = Balanco.objects.\
        values(ano=TruncYear('datas')).filter(Pagamento=True).\
        filter(Q(datas__month= 1)|Q(datas__month= 2)|Q(datas__month= 3)|Q(datas__month= 4)|Q(datas__month= 5)|Q(datas__month= 6))\
        .annotate(receita=Sum('receita'),despesa=Sum('despesa'),total=F("receita") - F("despesa")).order_by('-ano')



    # balancoSegundoSemestre = Balanco.objects.raw('''SELECT DISTINCT 1 as id,to_char(processos_balanco."datas", 'YYYY') as ano,
    #                                                     sum(receita) as rendimento,
    #                                                     sum(despesa) as despesa, (sum(receita) - sum(despesa)) as total
    #                                                     FROM public.processos_balanco  where
    #                                                      processos_balanco."Pagamento" = true and
    #                                                     (to_char(processos_balanco."datas", 'MM') = '07'
    #                                                     or to_char(processos_balanco."datas", 'MM') = '08' or
    #                                                     to_char(processos_balanco."datas", 'MM') = '09' or
    #                                                      to_char(processos_balanco."datas", 'MM') = '10' or
    #                                                      to_char(processos_balanco."datas", 'MM') = '11' or
    #                                                      to_char(processos_balanco."datas", 'MM') = '12')
    #                                                       GROUP BY to_char(processos_balanco."datas", 'YYYY') ''')


    balancoSegundoSemestre = Balanco.objects.\
        values(ano=TruncYear('datas')).filter(Pagamento=True).\
        filter(Q(datas__month= 7)|Q(datas__month= 8)|Q(datas__month= 9)|Q(datas__month= 10)|Q(datas__month= 11)|Q(datas__month= 12))\
        .annotate(receita=Sum('receita'),despesa=Sum('despesa'),total=F("receita") - F("despesa")).order_by('-ano')


    balancoCompleto = Balanco.objects.all().order_by('-datas')

    # somatorioGeral = Balanco.objects.raw('''SELECT DISTINCT  1 as id,
    #                                 sum(receita) as rendimento,  sum(despesa) as despesa,
    #                                   (sum(receita) - sum(despesa)) as total FROM
    #                                     public.processos_balanco
    #                                     WHERE processos_balanco."Pagamento" = true ''')

    somatorioGeral = Balanco.objects.\
        filter(Pagamento=True).aggregate(receitas=Sum('receita'),despesas=Sum('despesa'), total=Sum(F('receita')-F('despesa')))


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
        'balancoPrimeiroSemestre':balancoPrimeiroSemestre,
        'balancoSegundoSemestre':balancoSegundoSemestre,
        'somatorioGeral':somatorioGeral,

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
def faltasReunioes(request):
    faltas = Reuniao.objects.raw('''SELECT 1 as id, to_date(to_char(processos_reuniao."dataReuniao", 'MM YYYY'), 'MM YYYY') as mes,
                                    processos_usuario."Nome", count(processos_usuario."Nome") as faltas
                                    FROM  public.processos_reuniao, public.processos_reuniao_ausencia, 
                                    public.processos_usuario WHERE 
                                    processos_reuniao.id = processos_reuniao_ausencia.reuniao_id AND
                                      processos_usuario.id = processos_reuniao_ausencia.usuario_id
                                       group by processos_usuario."Nome", 
                                       to_char(processos_reuniao."dataReuniao", 'MM YYYY')
                                         order by to_char(processos_reuniao."dataReuniao", 'MM YYYY') desc''')
    form = ReuniaoForm()
    context = {
        'form':form,
        'faltas': faltas
    }

    return render(request, 'faltas.html', context)