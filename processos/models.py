from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from ckeditor.fields import RichTextField
from django.core.mail import send_mail

FUNCAO_CHOICE = (
    ('PROP','Proprietario'),
    ('PRE', 'Presidencia'),
    ('MAR', 'Marketing'),
    ('ADM','Adm/Financeiro'),
    ('PRO', 'Projetos'),
    ('RH', 'Recursos Humanos'),
)

FUNCAO_CHOICE_DESPESA = (
    ('DOM','Domínio'),
    ('SN','Simples-Nacional'),
    ('HOSP', 'Hospedagem'),
    ('ISS', 'ISS'),
    ('MUL', 'Multa'),
    ('OUT', 'Outros'),
)

FUNCAO_CHOICE_MESES = (
    ('01','Janeiro'),
    ('02','Fevereiro'),
    ('03', 'Março'),
    ('04', 'Abril'),
    ('05', 'Maio'),
    ('06', 'Junho'),
    ('07', 'Julho'),
    ('08', 'Agosto'),
    ('09', 'Setembro'),
    ('10', 'Outubro'),
    ('11', 'Novembro'),
    ('12', 'Dezembro'),
)

FUNCAO_CHOICE_PARCELAMENTO = (
    (1,'01-A VISTA'),
    (2,'02'),
    (3, '03'),
    (4, '04'),
    (5, '05'),
    (6, '06'),
    (7, '07'),
    (8, '08'),
    (9, '09'),
    (10, '10'),
    (11, '11'),
    (12, '12'),

)

GENERO_CHOICE = (
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('N', 'Não Declarado'),
)

UF = (
    ('MG', 'Minas Gerais'),
    ('SP', 'São Paulo'),
    ('RJ', 'Rio de Janeiro'),
    ('ES', 'Espirito Santo'),
    ('BA', 'Bahia'),
)

STATUS = (
    (0, 'Iniciado'),
    (1, 'Em andamento'),
    (2, 'Pendente'),
    (3, 'Resolvido'),
)

FUNCAO_CHOICE_SERVICO = (
    ('SPA','Single Page Application'),
    ('PWA','Progressive Web Application'),
    ('WS', 'WebSite'),
    ('SW', 'Sistema Web'),
    ('IV', 'Identidade Visual'),
)

FUNCAO_CHOICE_REUNIAO = (
    ('GERAL', 'GERAL'),
    ('DIRETORIA', 'DIRETORIA'),
    ('PROJETOS', 'PROJETOS'),
    ('EXTERNA', 'EXTERNA'),
)


class UsuarioManager(BaseUserManager):
    def create_user(self, Login, Nome, Situacao, CPF, Email, Funcao, password=None):
        user = self.model(
            Login=Login,
            Nome=Nome,
            Situacao=Situacao,
            CPF=CPF,
            Email=Email,
            Funcao=Funcao
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Login, Nome, Situacao, CPF, Email, Funcao, password):
        user = self.create_user(
            Login,
            Nome,
            Situacao,
            CPF,
            Email,
            Funcao
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    """Model definition for Usuario."""

    Nome = models.CharField('Nome', max_length=80)
    Foto = models.ImageField('Foto', upload_to='profile',blank=True, null=True)
    Login = models.CharField('Login', max_length=50, unique=True)
    password = models.CharField('Senha', max_length=128)
    Matricula = models.CharField('Matricula', max_length=128)
    Situacao = models.BooleanField('Ativo', default=True)
    CPF = models.CharField('CPF', max_length=20)
    RG = models.CharField('RG', max_length=20)
    nascimento = models.DateField('Nascimento', blank=True, null=True)
    Bairro = models.CharField('Bairro', max_length=100)
    Rua = models.CharField('Rua', max_length=100)
    N = models.CharField('Número', max_length=10)
    cidade = models.CharField('Cidade', max_length=10)
    CEP = models.CharField('CEP', max_length=50)
    Email = models.EmailField('Email', max_length=254)
    Celular = models.CharField('Celular', max_length=50, blank=True, null=True)
    Facebook = models.CharField('Facebook link', max_length=120, null=True, blank=True)
    Instagram = models.CharField('Instagram link', max_length=120, null=True, blank=True)
    LinkedIn = models.CharField('LinkedIn link', max_length=120, null=True, blank=True)
    Funcao = models.CharField('Função', max_length=4, choices=FUNCAO_CHOICE)

    # campos necessários pra o DJango
    last_login = models.DateTimeField(
        'Último login', blank=True, null=True, db_column='last_login')
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Membro da Equipe', default=False)
    is_admin = models.BooleanField('Administrador', default=False)

    USERNAME_FIELD = 'Login'
    EMAIL_FIELD = 'Email'
    REQUIRED_FIELDS = ['Nome', 'Situacao', 'CPF', 'Email', 'Funcao']

    objects = UsuarioManager()

    '''@receiver(post_save, sender=Usuario)
def post_usuario(self, instance, *args, **kwargs):
    if not Usuario.objects.filter(instance.Nome).exist():
        u = instance.Usuario.save()'''



    @property
    def is_superuser(self):
        return self.is_admin

    def get_full_name(self):
        return self.Nome

    class Meta:
        """Meta definition for Usuario."""

        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


    def nome(self):
        """Unicode representation of Usuario."""
        return self.Nome

    def __str__(self):
        """Unicode representation of Usuario."""
        return self.Nome.upper()

class Cliente(models.Model):

    nome = models.CharField(_('Nome'), max_length=40, null=True, blank=True)
    cidade = models.CharField(_('Cidade'), max_length=80, null=True, blank=True)
    bairro = models.CharField(_('Bairro'), max_length=80, null=True, blank=True)
    rua = models.CharField(_('Rua'), max_length=80, null=True, blank=True)
    numero = models.CharField(_('Numero'), max_length=20, null=True, blank=True)
    cep = models.CharField(_('CEP'), max_length=15, null=True, blank=True)
    cpf = models.CharField(_('CPF/CNPJ'), max_length=15, null=True, blank=True)
    contato = models.CharField(_('Contato'), max_length=20, null=True, blank=True)
    email = models.CharField(_('Email'), max_length=40, null=True, blank=True)

    class Meta:
        verbose_name = _("Cliente")
        verbose_name_plural = _("processos")


    def __str__(self):
        return self.nome

class Servico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='Cliente')
    nomeServico = models.CharField('Serviço', max_length=4, choices=FUNCAO_CHOICE_SERVICO)
    descricao = models.TextField('Descrição', null=True, blank=True)
    valor = models.DecimalField('Valor', max_digits=6, decimal_places=2)
    Desconto = models.DecimalField('Desconto',max_digits=6, decimal_places=2)
    parcelamento = models.IntegerField('Parcelado', choices=FUNCAO_CHOICE_PARCELAMENTO)

    def valorFinal(self):
        return str(self.valor - self.Desconto)

    def __str__(self):
        return self.nomeServico + ' - ' + str(self.cliente) + ' - R$' + str(self.valor - self.Desconto) + ' - ' + str(self.parcelamento) + 'x'


class Projeto(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='Servicos')
    repositorio = models.URLField(("Repositorio"),max_length=128)
    dataEntrega = models.DateField('Entrega', blank=True, null=True)
    status = models.IntegerField('Status', choices=STATUS)
    responsaveis = models.ManyToManyField('Usuario', null=True, blank=True, related_name="responsaveis")



class Reuniao(models.Model):
    dataReuniao = models.DateField('Data da Reunião', blank=True, null=True)
    tipoReuniao = models.CharField('Reunião', max_length=12, choices=FUNCAO_CHOICE_REUNIAO)
    descricaoReuniao = models.TextField('Descrição', null=True, blank=True)
    presenca = models.ManyToManyField('Usuario', null=True, blank=True, related_name="presenca")
    ausencia = models.ManyToManyField('Usuario', null=True, blank=True, related_name="ausencia")

    # def email(self):
    #     return ",".join([str (u) for u in self.presenca.all()])

    def reuniao(self):
        if self.tipoReuniao == 'GERAL':
            return 'GERAL - ' + str(self.dataReuniao.strftime("%d/%m/%Y"))
        elif self.tipoReuniao == 'DIRETORIA':
            return 'DIRETORIA - '+ str(self.dataReuniao.strftime("%d/%m/%Y"))
        elif self.tipoReuniao == 'PROJETOS':
            return 'PROJETOS - '+ str(self.dataReuniao.strftime("%d/%m/%Y"))
        elif self.tipoReuniao == 'EXTERNA':
            return 'EXTERNA - '+ str(self.dataReuniao.strftime("%d/%m/%Y"))

    def __str__(self):
        if self.tipoReuniao == 'GERAL':
            return 'GERAL - ' + str(self.dataReuniao.strftime("%d/%m/%Y"))
        elif self.tipoReuniao == 'DIRETORIA':
            return 'DIRETORIA - '+ str(self.dataReuniao.strftime("%d/%m/%Y"))
        elif self.tipoReuniao == 'PROJETOS':
            return 'PROJETOS - '+ str(self.dataReuniao.strftime("%d/%m/%Y"))
        elif self.tipoReuniao == 'EXTERNA':
            return 'EXTERNA - '+ str(self.dataReuniao.strftime("%d/%m/%Y"))

class Ata(models.Model):
    Reuniao = models.ForeignKey(Reuniao, on_delete=models.CASCADE, related_name='Reuniao')
    dataPublicacao = models.DateField('data', blank=True, null=True)
    Arquivo = models.FileField('Arquivo',upload_to= "Files", default="",blank=True, null=True)
    texto = RichTextField(null=True, blank=True)



class Receita(models.Model):
    Servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='servico')
    Data = models.DateField('Data',blank=True, null=True)
    valorParcela = models.DecimalField('Valor da Parcela', max_digits=6, decimal_places=2)
    Pagamento = models.BooleanField('Pagamento Efetuado', default=True)
    parcela = models.CharField('Parcela', max_length=20)

    class Meta:
        verbose_name = _("Receita")
        verbose_name_plural = _("Rerceitas")



class Despesas(models.Model):
    despesa = models.CharField('Despesa',max_length=40, null=True, blank=True)
    data = models.DateField('data', blank=True, null=True)
    valor = models.DecimalField('valor', max_digits=6, decimal_places=2)
    Pagamento = models.BooleanField('Pagamento Efetuado', default=True)

    class Meta:
        verbose_name = _("Despesa")
        verbose_name_plural = _("Despesas")


class Balanco(models.Model):
    receitas_id = models.IntegerField('receitas_id', blank=True, null=True)
    despesa_id = models.IntegerField('despesa_id', blank=True, null=True)
    receita = models.DecimalField('receita', max_digits=6, decimal_places=2,blank=True, null=True)
    despesa = models.DecimalField('despesa', max_digits=6, decimal_places=2,blank=True, null=True)
    datas = models.DateField('datas', blank=True, null=True)
    Pagamento = models.BooleanField('Pagamento Efetuado', default=True)

    class Meta:
        verbose_name = _("Balanco")
        verbose_name_plural = _("Balanco")

    #POST SAVE UTILIZADO PARA SALVAR DADOS CADASTRADOS EM RECEITA E DESPESAS
    #PARA FACILITAR CALCULOS E CONSULTAS
    @receiver(post_save,sender=Receita)
    def salvar_rendimento(sender,instance,created, **kwargs):
        receita = Balanco()
        receita.receitas_id = instance.pk
        receita.datas = instance.Data
        receita.receita = instance.valorParcela
        receita.despesa = 0.0
        receita.Pagamento = instance.Pagamento
        receita.save()

    @receiver(post_save,sender=Despesas)
    def salvar_despesa(sender,instance,created, **kwargs):
        despesa = Balanco()
        despesa.despesa_id = instance.pk
        despesa.datas = instance.data
        despesa.despesa = instance.valor
        despesa.receita = 0.0
        despesa.Pagamento = instance.Pagamento
        despesa.save()


    def __str__(self):
        return str(self.datas)

class Ouvidoria(models.Model):
    data = models.DateField('data', blank=True, null=True)
    texto = RichTextField(null=True, blank=True)

    def __str__(self):
        return str(self.data)

class Aviso(models.Model):
    membros = models.ManyToManyField('Usuario', null=True, blank=True, related_name="usuario")
    Data = models.DateField('Data', blank=True, null=True)
    assunto = models.CharField('Assunto', max_length=20, blank=True, null=True)
    descricao = models.TextField('Descrição', null=True, blank=True)

