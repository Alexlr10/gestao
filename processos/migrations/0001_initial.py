# Generated by Django 2.0 on 2020-05-05 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nome', models.CharField(max_length=80, verbose_name='Nome')),
                ('Foto', models.ImageField(default=None, upload_to='profile', verbose_name='Foto')),
                ('Login', models.CharField(max_length=50, unique=True, verbose_name='Login')),
                ('password', models.CharField(max_length=128, verbose_name='Senha')),
                ('Situacao', models.BooleanField(default=True, verbose_name='Ativo')),
                ('CPF', models.CharField(max_length=20, verbose_name='CPF')),
                ('RG', models.CharField(blank=True, max_length=20, null=True, verbose_name='RG')),
                ('Rua', models.CharField(blank=True, max_length=100, null=True, verbose_name='Rua')),
                ('N', models.CharField(blank=True, max_length=10, null=True, verbose_name='Número')),
                ('CEP', models.CharField(blank=True, max_length=50, null=True, verbose_name='CEP')),
                ('Email', models.EmailField(max_length=254, verbose_name='Email')),
                ('Celular', models.CharField(blank=True, max_length=50, null=True, verbose_name='Celular')),
                ('Data_de_Nascimento', models.DateField(blank=True, null=True, verbose_name='Data de Nascimento')),
                ('Data_de_Admissão', models.DateField(blank=True, null=True, verbose_name='Data de Admissão')),
                ('Data_de_Demissão', models.DateField(blank=True, null=True, verbose_name='Data de Demissão')),
                ('Complemento', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento')),
                ('Salario', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='Salário')),
                ('INSS', models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True, verbose_name='INSS')),
                ('Comissao', models.BooleanField(default=True, verbose_name='Recebe comissão')),
                ('Agencia', models.CharField(blank=True, max_length=50, null=True, verbose_name='Agência')),
                ('Conta_Corrente', models.CharField(blank=True, max_length=50, null=True, verbose_name='Conta')),
                ('Data_cadastro', models.DateTimeField(blank=True, null=True, verbose_name='Data de Cadastro')),
                ('Proximas_ferias', models.CharField(blank=True, max_length=50, null=True, verbose_name='Próximas férias')),
                ('Periodo_de_afastamento', models.CharField(blank=True, max_length=50, null=True, verbose_name='Período de afastamento')),
                ('Funcao', models.CharField(choices=[('PROP', 'Proprietario'), ('ADM', 'Administrador'), ('USU', 'Usuario'), ('MED', 'Médico'), ('FARM', 'Farmaceutico'), ('NUT', 'Nutricionista'), ('PSI', 'Psicólogo')], max_length=4, verbose_name='Função')),
                ('last_login', models.DateTimeField(blank=True, db_column='last_login', null=True, verbose_name='Último login')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Membro da Equipe')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Administrador')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
        ),
        migrations.CreateModel(
            name='Balanco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compras_id', models.IntegerField(blank=True, null=True, verbose_name='compras_id')),
                ('despesa_id', models.IntegerField(blank=True, null=True, verbose_name='despesa_id')),
                ('compra', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='compra')),
                ('despesa', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='despesa')),
                ('datas', models.DateField(blank=True, null=True, verbose_name='datas')),
            ],
            options={
                'verbose_name': 'Balanco',
                'verbose_name_plural': 'Balanco',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=40, null=True, verbose_name='Nome')),
                ('cidade', models.CharField(blank=True, max_length=80, null=True, verbose_name='Cidade')),
                ('bairro', models.CharField(blank=True, max_length=20, null=True, verbose_name='Bairro')),
                ('rua', models.CharField(blank=True, max_length=80, null=True, verbose_name='Rua')),
                ('numero', models.CharField(blank=True, max_length=20, null=True, verbose_name='Numero')),
                ('cep', models.CharField(blank=True, max_length=15, null=True, verbose_name='CEP')),
                ('cpf', models.CharField(blank=True, max_length=15, null=True, verbose_name='CPF/CNPJ')),
                ('contato', models.CharField(blank=True, max_length=20, null=True, verbose_name='Contato')),
                ('email', models.CharField(blank=True, max_length=20, null=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'processos',
            },
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantCompra', models.IntegerField(blank=True, null=True, verbose_name='Quantidade')),
                ('Data', models.DateField(blank=True, null=True, verbose_name='Data')),
                ('Desconto', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Desconto')),
                ('Cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Clientes', to='processos.Cliente')),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
            },
        ),
        migrations.CreateModel(
            name='Despesas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('despesa', models.CharField(choices=[('ICMS', 'ICMS'), ('SN', 'Simples-Nacional'), ('GAS', 'Gasolina'), ('PROD', 'Produtos'), ('INSS', 'INSS')], max_length=4, verbose_name='Despesa')),
                ('data', models.DateField(blank=True, null=True, verbose_name='data')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='valor')),
            ],
            options={
                'verbose_name': 'Despesa',
                'verbose_name_plural': 'Despesas',
            },
        ),
        migrations.CreateModel(
            name='Lote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroLote', models.IntegerField(blank=True, null=True, verbose_name='Nº do lote')),
                ('quantLote', models.IntegerField(blank=True, null=True, verbose_name='Quantidade')),
            ],
            options={
                'verbose_name': 'Lote',
                'verbose_name_plural': 'Lotes',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomeproduto', models.CharField(blank=True, max_length=30, null=True, verbose_name='Produto')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descrição')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.AddField(
            model_name='lote',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produto', to='processos.Produto'),
        ),
        migrations.AddField(
            model_name='compra',
            name='Produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Produtos', to='processos.Produto'),
        ),
    ]
