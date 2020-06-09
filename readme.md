# Gestao Interna Next Step

## Instalar o docker em sua maquina Windows 10 PRO

1. Faça o download do instalador a partir do link:
   
   https://www.docker.com/get-started

2. Faça a instalação e seguindo a instalação padrão

3. Abra a aplicaçao pelo icone na area de trabalho e abra a interface
   clicando no submenu proximo ao relogio e clicando com o botao direto abra a dashboard.



## Instalar o docker em sua maquina Linux

1. Atualize seu Sistema
   O sistema precisa ser atualizado para você ter mais segurança e confiabilidade para a instalação do Docker. 
   Execute os dois comandos abaixo:

   sudo apt update

   sudo apt upgrade

2. Instale Pacotes Pré-requisitos
   Assim que atualizar o sistema, você deve instalar alguns dos pacotes necessários antes de instalar o Docker Ubuntu. 
   Você pode fazer isso com a ajuda de um único comando:
  
   sudo apt-get install  curl apt-transport-https ca-certificates software-properties-common

3. Adicione os Repositórios do Docker
   Agora você tem adicionar os repositórios do Docker. 
   Isso vai fazer com que o processo de instalação seja muito mais fácil.
   Isso habilita você a usar o método oficial suportado de instalação.
   
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

   Agora, adicione o repositório executando este comando:

   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

   Depois disso, apenas atualize a informação do repositório

   sudo apt update

4. Instalar Docker
   Estamos quase terminando. Use o comando para, enfim, instalar o Docker em sua maquina.
   
   sudo apt install docker-ce

5. Verificar Status do Docker
   Assim que a instalação estiver completa, é uma ótima ideia verificar o status do serviço.

   sudo systemctl status docker

## Iniciar um novo projeto com base neste repositório

1. Clone este repositório e acesse ele.
    
   git clone https://github.com/NextStepSI/gestao_interna.git
   cd gestao_interna


2. Habilitar conexão com o banco de dados 

   Entre na pasta legacy na raiz do projeto e abra o arquivo settings.py e descomente o tredo de codigo abaixo:
   
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
      }
   }
 

## Implantação

1. Inicie o stack docker
 
   docker-compose build

   Apos carregar o download de todas as dependencias execute o comando
  
   docker-compose up
   
   Crie seu super usuario com o comando 

   docker-compose run web python manage.py createsuperuser

   Nos atributos de superusuario e obrigatorio Situaçao = 1 e Funcao = PROP

   Abra seu navegador com a url localhost:8000

`
