Um aplicativo de gerência de patentes, escrita em Django, para o Instituto Federal de Goiás.
Passos para instalar:
* Criar banco 'ifgapp' em PostgreSQL.
* cd c:\dev\ifgapp\ifg
* Executa 'python manage.py flush'
* Executa 'python manage.py syncdb --noinput' (This will create the model and some initial data)
* Executa 'python manage.py carga_ifgapp'
* Executa 'python manage.py runserver' para executar o app usando o webserver embutido do Django

ver 0.1
-----------------------------
- Criar Gerência de Usuários
- Criar Testes de Usuários
- Criar CRUD de Usuários (servidores e pesquisadores) e Grupos de permissões
- Criar CRUD básico de Tecnologia

ver 0.2
-----------------------------
- CRUD Tecnologia: Dados gerais, Nome, Categorias, Número de Protocolo
- CRUD Instituição

ver 0.3 (PLANNED 08/11)
-----------------------------
- Finalizar CRUD Tecnologia

ver 0.4 (PLANNED 15/11)
-----------------------------
- Finalizar CRUD Inventor

ver 0.4 (PLANNED 22/11)
-----------------------------
- Utilidade de busca de institução por nome ou sigla
- Utilidade de busca de pessoa por nome










