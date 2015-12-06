Um aplicativo de gerência de patentes, escrita em Django 1.6.10 e Python 2.7, para o Instituto Federal de Goiás.
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

ver 0.3
-----------------------------
- CRUD Tecnologia
(somente suporte para anexos em PDF, e somente podemos anexar na edição, não no cadastro inicial).
- CRUD Inventor (exceto cadastro de anexos).

ver 0.4
-----------------------------
- Suporte para anexar/atualizar/baixar arquivos no formulário de cadastro.
- CRUD Tarefa.
- CRUD Contrato de Transferência de Tecnologia.
- Adicionar anexos no cadastro de Inventor

ver 0.5
-----------------------------
- Suporte para campos excludentes (p.ex: Inventor/Vínculo IFG/Instituição).
- Adicionar suporte para anexos em formato Imagem (GIF, JPG, PNG) e Texto.
- Ordenar a lista de Tecnologias por nome.

ver 0.6 (PLANNED 29/11)
-----------------------------
- Valiar telefone. -> ok
- Utilidade de busca de Institução por nome ou sigla. -> ok
- Utilidade de busca de Inventor por nome. -> ok
- BUG: nome de arquivo anexado superior a 100 caracteres

ver 0.7 (PLANNED 06/12)
-----------------------------
- Ferramenta de busca de Tecnologia.

ver 0.8 (PLANNED 13/12)
-----------------------------
- Ferramenta de busca de Inventor.
- Ferramenta de busca de Instituição.
- Ferramenta de busca de Tarefa.
- Ferramenta de busca de Contrato de Transferência de Tecnologia.

ver 0.9 (PLANNED 20/12)
-----------------------------
- Automatização de Tarefas.

ver 0.10 (PLANNED 27/12)
-----------------------------
- Unificar os caminhos onde os anexos são salvados. Atualmente tem dois.
- Permitir salvar os anexos antes de o objeto ser salvado (usar o nome único).
- Bug: Criar uma Tecnologia, então aparece a lista de Tecnologias, clicar no Next.. o form aparece de novo.
















