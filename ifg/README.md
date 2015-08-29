Um aplicativo de gerência de patentes, escrita em Django, para o Instituto Federal de Goiás.
Passos para instalar:
* Criar banco 'ifgapp' em PostgreSQL.
* Executa 'python manage.py flush'
* Executa 'python manage.py syncdb --noinput' (This will create the model and some initial data)
* Executa 'python manage.py runserver' para executar o app usando o webserver embutido do Django

ver 0.1
-----------------------------
- Criar Gerência de Usuários -> ok
- Criar Testes de Usuários -> ok
- Criar CRUD de Usuários (servidores e pesquisadores) e Grupos de permissões -> ok
-
