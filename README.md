# Ensalamento Icet

Este projeto é uma solução para a criação de ensalamento dinâmico na universidade, com foco em melhorar a alocação de salas e horários para as disciplinas por meio de uma aplicação web e inteligencia artificial, 
otimizando o uso dos espaços físicos e melhorando o desempenho acadêmico.

[Documentação](Docs/Documentoderequisitos.pdf)

![Home](Docs/home.png)

## Sumário
- Introdução
- Funcionalidades
- Instalação
- Tecnologias Utilizadas

## Introdução
Este projeto foi desenvolvido para automatizar o processo de ensalamento na Universidade Federal do Amazonas, substituindo o método manual de uso de tabelas no Excel por uma solução mais eficiente utilizando tecnicas de aprendizado de maquina. A proposta é reduzir o tempo gasto na preparação e ajustes, proporcionando uma melhor organização dos horários e salas disponíveis para professores e alunos.

## Funcionalidades principais
- **Gerenciamento de Usuários**: Cadastrar, alterar e desativar usuários do sistema.
- **Gerenciamento de Disciplinas**: Manter informações sobre as disciplinas oferecidas.
- **Gerenciamento de Espaços Físicos**: Manter registro das salas e laboratórios disponíveis.
- **Gerar Alocações de Espaços Físicos**: Realizar o ensalamento das disciplinas.
- **Geração de Relatórios**: Gerar relatórios de ensalamento que incluem dados como sala, horário, disciplina e docente.
- **Disponibilidade de Espaços**: Visualizar horários e salas/laboratórios disponíveis para os usuários.

## Instalação
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
2. Instale as dependências do projeto em um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. Configure o banco de dados(Settings.py)
   ```bash
   DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
   }
4. Migre as tabelas para o banco de dados
   ```bash
   python manage.py migrate
5. Inicie o servidor:
   ```bash
   python manage.py runserver

## Tecnologias Utilizadas
- **Linguagem de Programação:** Python, JavaScript.
- **Framework**: Django (arquitetura MTV).
- **Banco de Dados**: MySQL.
- **Outros:** Sklearn, HTML, CSS, Bootstrap.
