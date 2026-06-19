# Projeto Final de Grafos

Este projeto foi feito para a avaliação final da disciplina de Grafos.

A ideia foi representar uma situação parecida com uma malha logística, em que algumas cidades estão ligadas por rotas. Cada cidade virou um vértice do grafo, e cada rota entre duas cidades virou uma aresta.

As rotas possuem peso, que neste caso representa a distância em quilômetros.

## Tema do projeto

O tema escolhido foi uma rede de cidades conectadas por rotas de transporte.

No grafo:

* os vértices representam cidades;
* as arestas representam rotas entre essas cidades;
* os pesos representam a distância aproximada em quilômetros.

O grafo é não direcionado, porque considerei que uma rota pode ser usada nos dois sentidos. Por exemplo, se existe uma ligação entre Jundiaí e Campinas, também é possível voltar de Campinas para Jundiaí.

## Representação usada

O grafo foi implementado usando lista de adjacência.

Escolhi essa estrutura porque nem todas as cidades estão conectadas diretamente entre si. Então faz mais sentido guardar apenas as rotas que existem.

Se fosse usada uma matriz de adjacência, seria necessário reservar espaço para todas as combinações possíveis entre cidades, mesmo quando não existe rota entre elas. Para esse projeto, a lista de adjacência ficou mais simples e econômica.

## Algoritmos implementados

### Busca em largura

A busca em largura foi usada para percorrer o grafo a partir de uma cidade inicial.

Com ela, dá para ver quais cidades podem ser alcançadas e quantas ligações são necessárias para chegar até cada uma.

Esse algoritmo usa uma fila para controlar a ordem de visita dos vértices.

### Dijkstra

O algoritmo de Dijkstra foi usado para encontrar o menor caminho entre duas cidades.

Como as rotas têm peso, ele soma os custos dos trechos e encontra a rota com menor distância total.

Neste projeto, o menor custo significa o menor caminho em quilômetros.

### Prim

Também foi implementado o algoritmo de Prim para gerar uma árvore geradora mínima.

A ideia é encontrar um conjunto de rotas que conecte todas as cidades gastando o menor custo total possível, sem criar caminhos desnecessários.

## Estrutura do projeto

text
grafo_logistica/
├── data/
│   ├── cidades.csv
│   └── rotas.csv
├── src/
│   ├── grafo.py
│   └── main.py
├── README.md
└── relatorio.md


O arquivo rotas.csv guarda as ligações entre as cidades e o custo de cada rota.

O arquivo grafo.py tem a estrutura do grafo e os algoritmos.

O arquivo main.py carrega os dados e executa o programa.

## Como executar

Para rodar o projeto, é necessário ter o Python instalado.

Depois de baixar ou clonar o repositório, entre na pasta do projeto:

bash
cd grafo_logistica


Depois execute:

bash
python src/main.py


Se esse comando não funcionar, tente:

bash
python3 src/main.py


## Usando outras cidades

O programa também permite escolher a origem e o destino pelo terminal.

Exemplo:

bash
python src/main.py --origem "Jundiai" --destino "Santos"


Outro exemplo:

bash
python src/main.py --origem "Campinas" --destino "Mogi das Cruzes"


## Exemplo de saída

Um dos resultados esperados é:

text
Menor custo de Jundiai até Santos: 135 km
Rota: Jundiai -> Sao Paulo -> Santos


Isso significa que, considerando as rotas cadastradas no arquivo CSV, o menor caminho entre Jundiaí e Santos passa por São Paulo.

## Como alterar os dados

Para testar outro cenário, basta editar o arquivo:

text
data/rotas.csv


O formato usado é este:

csv
origem,destino,custo_km
Jundiai,Campinas,40
Campinas,Americana,35


Depois de alterar o arquivo, basta executar o programa novamente.

## Considerações finais

Esse projeto mostra uma forma simples de aplicar grafos em um problema parecido com logística e transporte.

Em sistemas reais, como aplicativos de mapa, redes de entrega ou sistemas de roteirização, a mesma lógica é usada em uma escala muito maior. O maior desafio seria lidar com muitos vértices e arestas, além de mudanças constantes nas rotas, custos e condições do caminho.
