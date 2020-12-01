# Sistema de Controle de Carga e Descarga de Mercadorias
![](/carga_descarga/core/static/imagens/logo.png)

### Sistema para automatizar o processo de carga e descarga de mercadorias da Fribel Comércio de Alimentos Ltda.

#### Características:
- Sistema web
- Sistema criado com Python (Django), HTML 5, CSS e JavaScript
- Sistema com gerenciamento de permissão de acesso via autenticação
- Sistema conectado com outros sistemas para importação de informações

#### Funcionalidades:
- Autenticação
- Listagem de cargas
- CRUD de cargas
- Alerta de conflito de cargas marcadas para descarga no mesmo dia
- Alerta de liberação de carga
- Detalhamento de cargas com informações de nota fiscal e banco de dados 

#### Dados principais:
|Atributos|
|--------------------|
|Dados principais|Dados adicionais|
|-----------|----------|
|Número da nota fiscal|Tipo de entrada|
|Indústria|Produto| 
|Dia de descarga|Quantidade|
|Status|Movimentação|
||Frete|
||Observação|
||Box|
||Unidade|

