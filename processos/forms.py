from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext as _
from .models import *
from . import models


class UsuarioCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Senha'), widget=forms.TextInput(attrs={'type': 'password', 'id': 'password1'}))
    password2 = forms.CharField(label=_('Confirmação da senha'),
                                widget=forms.TextInput(attrs={'type': 'password', 'id': 'password2'}))

    class Meta:
        model = Usuario

        fields = ('Nome',
                  'Login',
                  'Situacao',
                  'CPF',
                  'RG',
                  'Bairro',
                  'Rua',
                  'N',
                  'cidade',
                  'CEP',
                  'nascimento',
                  'Matricula',
                  'Email',
                  'Celular',
                  'Facebook',
                  'Instagram',
                  'LinkedIn',
                  'Funcao',
                  'password1',
                  'password2',
                  )

        widgets = {

            'Situacao': forms.CheckboxInput(attrs={'id': 'situacao', 'onclick': 'myFunction()'}),
            'nascimento': forms.TextInput(attrs={'type': 'date'}),
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("As senhas não conferem"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioMeusDados(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=_('Senha'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('Confirmação da senha'), widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['Foto', 'Nome', 'Email', 'Matricula', 'CPF', 'RG', 'Celular', 'Login', 'password']

        widgets = {

            'Nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'Email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'Matricula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricula'}),
            'CPF': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'RG': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RG'}),
            'Celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular'}),
            'Login': forms.TextInput(attrs={'class': 'form-control', 'id': 'Login'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'Password'}),

        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("As senhas não conferem"))
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UsuarioChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )

    class Meta:
        model = Usuario
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = self.fields['password'].help_text.format(
            '../password/')
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UsuarioForm(forms.ModelForm):
    """Form definition for Filial."""

    class Meta:
        """Meta definition for Filialform."""

        model = Usuario
        fields = '__all__'

        widgets = {
            'Nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'Login': forms.TextInput(attrs={'class': 'form-control', 'id': 'Login'}),
            'Password': forms.TextInput(attrs={'class': 'form-control', 'id': 'Password'}),
            'Situacao': forms.TextInput(
                attrs={'type': 'checkbox', 'class': 'form-control', 'id': 'situacao', 'onclick': 'myFunction()'}),

        }

class MeusDadosForm(forms.ModelForm):
    """Form definition for Filial."""

    class Meta:
        """Meta definition for Filialform."""

        model = Usuario
        #fields = '__all__'
        fields = ['Foto','Nome','Email','Matricula','Rua','N','Bairro','cidade','CPF','RG','Celular','Login','password']

        widgets = {
            'Foto': forms.FileInput(),
            'Nome': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Nome'}),
            'Email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}),
            'Matricula': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Matricula'}),
            'Rua': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rua'}),
            'N': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número'}),
            'Bairro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'CPF': forms.TextInput(attrs={'class': 'form-control','placeholder': 'CPF'}),
            'RG': forms.TextInput(attrs={'class': 'form-control','placeholder': 'RG'}),
            'Celular': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Celular'}),
            'Login': forms.TextInput(attrs={'class': 'form-control', 'id': 'Login'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'Password'}),
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

        widgets = {

            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'id': 'cpf', 'placeholder': '___.___.___-__'}),
            'rua': forms.TextInput(attrs={'placeholder': 'Rua'}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Cidade'}),
            'numero': forms.TextInput(attrs={'placeholder': 'Numero'}),
            'cep': forms.TextInput(attrs={'placeholder': 'CEP'}),
            'contato': forms.TextInput(attrs={'placeholder': 'Contato'}),

            'email': forms.TextInput(attrs={'placeholder': 'E-mail '}),
        }


class ServicoForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Servico
        fields = '__all__'
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

            'Desconto': forms.TextInput(attrs={'type': 'number', 'step': 0.1, 'class': 'form-control', 'value': 0.0}),
        }


class ProjetoForm(forms.ModelForm):
    #SOBRESCREVE A VARIAVEL ORIGINAL COM OS DADOS DESEJADOS
    responsaveis = forms.ModelMultipleChoiceField(
        queryset=Usuario.objects.filter(
            Situacao=True).order_by('Nome'),
        widget=forms.SelectMultiple(attrs={'class': 'responsaveis'}))

    class Meta:
        model = Projeto
        fields = ['servico','repositorio','dataEntrega','status','responsaveis']

        widgets = {
            'servico': forms.Select(attrs={'class': 'servico', 'style': 'width:580px;','margin-top':'-4px', 'id': 'id_servico'}),
            'status': forms.Select(attrs={'class': 'status', 'id': 'id_status'}),
            'dataEntrega': forms.TextInput(attrs={'type': 'date'}),
            #'responsaveis': forms.SelectMultiple(attrs={'class':'responsaveis','id':'id_responsaveisss'}),

        }


class ReuniaoForm(forms.ModelForm):

    presenca = forms.ModelMultipleChoiceField(
        queryset= Usuario.objects.filter(
            Situacao=True).order_by('Nome'),
        widget=forms.SelectMultiple(attrs={'class':'presenca','style':'width:565px; height:200px;'}))
    ausencia = forms.ModelMultipleChoiceField(
        queryset= Usuario.objects.filter(Situacao=True).order_by('Nome'),
        required = False,
        widget=forms.SelectMultiple(attrs={'class':'presenca','style':'width:565px; height:200px;'}))


    class Meta:
        model = Reuniao
        fields =  ['dataReuniao','tipoReuniao','descricaoReuniao','presenca','ausencia']
        # exclude = ['data_cadastro', 'data_atualizacao']

        widgets = {

            'dataReuniao': forms.TextInput(attrs={'type': 'date', 'class': 'form-control', 'id': 'dataReuniao'}),
            'tipoReuniao': forms.Select(attrs={'id': 'tipoReuniao','class': 'form-control'}),
            'Arquivo' : forms.FileField(label='Select a file'),


         }



class AtaForm(forms.ModelForm):

    class Meta:
        model = Ata

        fields = ['Reuniao', 'dataPublicacao', 'Arquivo', 'texto']

        widgets = {
             'Reuniao': forms.Select(attrs={'class':'reuniao','style':'width:300px;','id':'id_Reuniao'}),
             'dataPublicacao': forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'id':'dataPublicacao','style':'width:300px;' }),
        }


class ReceitaForm(forms.ModelForm):

    class Meta:
        model = Receita
        fields = '__all__'


        widgets = {
            'Servico': forms.Select(attrs={'class': 'Servico', 'style': 'width:580px;', 'margin-top': '-4px', 'id': 'id_Servico'}),
            'Data': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Entrada': forms.TextInput(attrs={'type': 'number', 'step': 0.01, 'class': 'form-control', 'value': 0.0}),
            'valorParcela': forms.TextInput(
                attrs={'type': 'number', 'step': 0.01, 'class': 'form-control', 'value': 0.0}),
        }


class DespesasForm(forms.ModelForm):

    class Meta:
        model = Despesas
        fields = '__all__'

        widgets = {
            'despesa': forms.TextInput(attrs={'id': 'despesa'}),
            'data': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class BalancoForm(forms.ModelForm):
    # data_intimacao = forms.DateField(widget=forms.TextInput(attrs={'format': 'dd/mm/yyyy', 'type': 'date'}))

    class Meta:
        model = Balanco
        fields = '__all__'

        widgets = {

            'datas': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class OuvidoriaForm(forms.ModelForm):
    class Meta:
        model = Ouvidoria
        fields = ['data','texto']

        widgets = {
            ''
            'data': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class AvisoForm(forms.ModelForm):
    membros = forms.ModelMultipleChoiceField(queryset=Usuario.objects.filter(Situacao=True),widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Aviso
        fields = ['membros','Data','assunto','descricao']

        widgets = {
            'membros': forms.CheckboxSelectMultiple(),
            'Email': forms.TextInput(attrs={'class': 'form-control','id':'Email'}),
            'Data': forms.TextInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'type': 'textArea', 'class': 'form-control','style':'width:850px; height:200px;'}),
        }



