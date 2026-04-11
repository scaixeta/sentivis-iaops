# agroapi-primeiros-passos

## Página 1

PROCEDIMENTO DE ACESSO ÀS APIs DA PLATAFORMA AgroAPI – PRIMEIROS
PASSOS
CRIANDO UMA CONTA PARA ACESSO ÀS APIs DA PLATAFORMA
Se você ainda não possui uma conta na Plataforma AgroAPI, siga os passos abaixo
para criar uma.
1. Acesse a Loja de APIs (<https://www.agroapi.cnptia.embrapa.br/store/>) e utilize a
opção Criar conta na barra superior.
2. Siga as instruções da página seguinte, preenchendo as informações obrigatórias e
leia atentamente o Termo de Acesso e Uso da Plataforma.
1

## Página 2

CRIANDO UMA APLICAÇÃO E GERANDO AS CHAVES DE ACESSO PARA O CONSUMO DAS APIs
DA PLATAFORMA
Para consumir uma determinada API na Plataforma AgroAPI, você deve entrar na
Loja de APIs com sua credencial de acesso, formada pelo Login e Senha.
Você deve criar suas aplicações na Loja de APIs. Quando você registra a sua
aplicação na Loja de APIs, esta aplicação recebe uma chave de registro e um segredo
associado, que representam as credenciais da aplicação. A chave de registro torna-se o
identificador único da Aplicação, similar a um nome de usuário. A aplicação poderá utilizar
quaisquer APIs disponíveis na Loja. A criação de uma aplicação, bem como a subscrição
de uma determinada API é demonstrada na sequência.
Após realizar o acesso à Loja de APIs, você pode realizar o cadastro de suas
aplicações utilizando a opção APPLICATIONS no menu lateral esquerdo.
2

## Página 3

Na tela inicial são exibidas todas as suas aplicações já cadastradas. Ao realizar o
cadastro, é criada uma aplicação padrão denominada DefaultApplication. Esta aplicação
pode ser alterada ou excluída, de acordo com as suas necessidades. Para criar uma nova
aplicação, utilize a opção ADD APPLICATION localizada na barra superior. Na tela
seguinte, preencha o Nome e as demais informações da aplicação e pressione o botão
Add para concluir. Não são permitidos espaços e acentuação no Nome da aplicação.
3

## Página 4

4

## Página 5

Antes de fazer uma chamada a uma determinada API, você precisa gerar uma chave
de registro (Consumer Key) e um segredo associado (Consumer Secret), bem como um
Access Tokens. O Access Token é a credencial que será utilizada pela sua aplicação
para acesso à API. Ele é gerado utilizando a chave de registro e o segredo associado da
aplicação. Uma forma de obter todas as credenciais, de uma só vez, é por meio da Loja
de APIs, seção APPLICATIONS. Uma vez selecionada a Aplicação desejada, acesse as
abas Production Keys e Sanbox Keys, e clique sobre o botão Generate keys.
Observe que o token de acesso possui um tempo de validade de 60 minutos (3.600
segundos), por padrão. Caso deseje um tempo de validade indeterminado, preencha o
valor do campo Access token validity period com o valor -1.
5

## Página 6

A chave de registro (Consumer Key) e o segredo associado (Consumer Secret),
bem como o Access Token poderão ser visualizadas a partir do botão Show Keys.
6

## Página 7

CONSUMINDO UMA API NA PLATAFORMA DE MANEIRA INTERATIVA
Uma vez criada a aplicação e suas credenciais, mesmo antes de começar a
desenvolver sua primeira linha de código, é possível utilizar e avaliar as possibilidades
das APIs da Plataforma AgroAPI. Na página principal da Loja de APIs, selecione a API
desejada e vá até a aba Overview. Em seguida, escolha o plano desejado (por exemplo:
Gratuito1KPorMes) em Tiers e clique sobre o botão Subscribe.
Após a mensagem de confirmação da subscrição, clique sobre o botão Stay on this
page.
7

## Página 8

Em seguida, acesse a aba API Console da API. Observe que as informações da
Aplicação e do Access Token são preenchidas automaticamente.
Por último, comece a experimentar os recursos da API selecionada a partir da aba
API Console. Uma resposta de sucesso é exibida conforme abaixo.
8

## Página 9

CONSUMINDO UMA API NA PLATAFORMA DE MANEIRA PROGRAMÁTICA
Como dito anteriormente, antes de fazer uma chamada a uma determinada API,
você precisa gerar uma chave de registro (Consumer Key) e um segredo associado
(Consumer Secret). Uma vez criada a aplicação e suas credenciais, o Access Token pode
ser obtido de maneira programática a partir das instruções disponíveis na aba Production
Keys ou Sandbox Keys.
Com o Access Token, é possível consumir as informações de uma determinada API
vinculada a uma aplicação, conforme apresentado abaixo com o consumo do recurso
culturas da API Agritec.
9