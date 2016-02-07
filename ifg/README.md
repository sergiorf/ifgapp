Um aplicativo de gerência de patentes, escrita em Django 1.6.10 e Python 2.7, para o Instituto Federal de Goiás.
Passos para instalar:
* Criar banco 'ifgapp' em PostgreSQL.
* cd c:\dev\ifgapp\ifg
* Executa 'python manage.py flush'
* Executa 'python manage.py syncdb --noinput' (This will create the model and some initial data)
* Executa 'python manage.py carga_ifgapp'
* Executa 'python manage.py runserver' para executar o app usando o webserver embutido do Django
* Criar um cron (unix) ou um serviço (windows) para executar 'python manage.py maintain_tarefas'

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

ver 0.6
-----------------------------
- Validar telefone.
- Utilidade de busca de Instituição por nome ou sigla.
- Utilidade de busca de Inventor por nome.
- Utilidade de busca de Tecnologia por nome.
- BUG: nome de arquivo anexado superior a 100 caracteres

ver 0.7
-----------------------------
- Tela de busca de Tecnologia.
- Tela de busca de Inventor.
- Tela de busca de Instituição.
- Tela de busca de Tarefa.
- Tela de busca de Contrato de Transferência de Tecnologia.

ver 0.8
-----------------------------
- Atualizar código com a v10 do documento de especificações.
- Na classe Contrato, vincular categoria_tecnologia à Tecnologia escolhida.
- Initializar o status da tarefa automaticamente segundo as datas.
- Criei massa de dados para Tarefa.
- Criar um background task para setar o status da Tarefa = 'não realizada'. Criei o comando
  'maintain_tarefas'. Ele deve ser executado a intervalos regulares. A forma de executar, dependerá
  do SO em que será instalado a app (unix=cron, windows=at/services).
- Colocar intervalos de datas nas telas de busca (Tarefa, Tecnologia, Contrato).
- Bug: Form Tecnologia: Não pode ter a mesma pessoa em Criador e Co-criador.

ver 0.09
-----------------------------
- Remover a entidade Pesquisador.
- Criar a entidade MetaTarefa. Essa entidade contém a descrição das tarefas automáticas. O intuito é
criar as tarefas automáticas a partir de dados e não de código.

ver 0.10
-----------------------------
- Corrigir bug para visualizar páginas quando logado como superuser.
- Bug: Criar uma Tecnologia, então aparece a lista de Tecnologias, clicar no Next.. o form aparece de novo.
- Atualizações no modelo conforme à v.11 das especificações.

ver 0.11
-----------------------------
- Finalizar módulo de Tarefas automáticas.
- Criar grupos de teste.
- Bug: Typo no template de lista de grupos.
- Remover o modelo MetaTarefa (deprecated).
- Adicionar opção 'Servidores' no tab de navegação.
- Nos resultados da busca, ao invés de "editar" e "remover", gostaria que houvesse apenas um "ver detalhes",
  que, aliás, eu não sei onde está. Só consigo visualizar detalhes dos objetos clicando em "editar"
  e deixando inalterado.

ver 0.12
-----------------------------
- Mostrar messagem de erro: "usuário ou senha incorretos" quando login falha.
- Resolver questão com as tarefas automáticas de tipo Marca.
- Se possível, gostaria de diferenciar nos formulários de busca os resultados para quando
  não houver nenhuma tecnologia cadastrada, ou nenhuma tecnologia encontrada correspondente aos filtros.

ver 0.13
-----------------------------
-Criadores e CoCriadores de Tecnologias são PessoaFisica.
-Criar as seguintes permissões:
# VER_TECNOLOGIAS: If not present, user can't list tech. The tech option is not
present in the context menu.
# VER_TECNOLOGIAS_PROPRIAS: If present, user can only access her own techs
# MODIFICAR_TECNOLOGIAS: If present, user can edit techs
# VER_PESSOAS: If not present, user can't list pessoas. The pessoas options are not
present in the context menu.

# VER_PESSOAS_MESMO_GRUPO
# MODIFICAR_PESSOAS
# MODIFICAR_PESSOAS_MESMO_GRUPO
# VER_TAREFAS
# MODIFICAR_TAREFAS








