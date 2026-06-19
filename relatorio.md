# Relatório do Projeto — Grafo de Rotas Logísticas

## 1. Domínio escolhido

O domínio escolhido foi uma rede de rotas logísticas entre cidades. Esse cenário faz sentido como grafo porque existem pontos de entrega, centros de distribuição ou cidades que se conectam por meio de estradas.

No problema desenvolvido:

- cada vértice representa uma cidade ou ponto logístico;
- cada aresta representa uma rota entre duas cidades;
- cada aresta possui pesos: distância em quilômetros, tempo em minutos e custo em reais.

O grafo é não direcionado, porque uma rota entre duas cidades pode ser usada nos dois sentidos. Por exemplo, se existe uma rota entre Jundiaí e Campinas, considera-se que também é possível ir de Campinas para Jundiaí.

O grafo também é ponderado, pois as rotas possuem valores associados. Esses pesos permitem resolver problemas como encontrar o menor trajeto, o caminho mais rápido ou o caminho mais barato.

## 2. Representação do grafo em memória

A estrutura escolhida foi a lista de adjacência.

Nessa representação, cada cidade guarda uma lista com suas cidades vizinhas e os pesos das rotas. Essa escolha é adequada porque, em uma rede de cidades, cada cidade normalmente se conecta apenas a algumas outras cidades, e não a todas.

Se fosse usada uma matriz de adjacência, seria necessário guardar uma tabela com todas as combinações possíveis entre vértices. Para um grafo grande, isso consumiria muita memória, principalmente porque muitas posições ficariam vazias. Já a lista de adjacência guarda apenas as conexões que realmente existem, tornando o programa mais eficiente para grafos esparsos.

O grafo é montado a partir do arquivo `data/rotas.csv`, ou seja, os dados não ficam fixos diretamente no código. Assim, é possível alterar ou aumentar a rede de rotas apenas editando o arquivo CSV.

## 3. Travessia implementada

A travessia implementada foi a busca em largura, também chamada de BFS.

A BFS percorre o grafo por níveis. Primeiro ela visita a cidade de origem, depois todas as cidades diretamente conectadas a ela, depois as cidades conectadas a essas vizinhas, e assim por diante.

Para funcionar, a BFS utiliza uma fila como estrutura auxiliar. A fila garante que os vértices sejam processados na ordem em que foram descobertos.

No cenário logístico, a busca em largura permite descobrir todas as cidades alcançáveis a partir de uma cidade inicial. Também foi usada para verificar se existe caminho entre duas cidades.

A diferença principal entre BFS e DFS é que a BFS percorre por níveis, enquanto a DFS mergulha em profundidade por um caminho antes de voltar e explorar outros. A DFS normalmente usa pilha ou recursão, enquanto a BFS usa fila.

## 4. Caminho mínimo com Dijkstra

Como o grafo possui pesos, foi implementado o algoritmo de Dijkstra para encontrar o menor caminho entre duas cidades.

O Dijkstra calcula o caminho de menor custo a partir de uma origem até um destino. No programa, o usuário pode escolher qual peso deseja considerar:

- distância em quilômetros;
- tempo em minutos;
- custo em reais.

Na prática, isso permite responder perguntas diferentes. Se o peso escolhido for distância, o resultado representa a rota mais curta. Se o peso escolhido for tempo, representa a rota mais rápida. Se o peso escolhido for custo, representa a rota mais barata.

O algoritmo utiliza uma fila de prioridade para sempre expandir primeiro o vértice com menor custo acumulado conhecido até o momento.

## 5. Árvore Geradora Mínima com Kruskal

Também foi implementado o algoritmo de Kruskal para gerar uma árvore geradora mínima.

A ideia da árvore geradora mínima é conectar todos os vértices do grafo com o menor custo total possível, sem formar ciclos. No cenário logístico, isso pode representar um planejamento mínimo de rotas, cabos, contratos de transporte ou conexões necessárias para manter todas as cidades ligadas.

O Kruskal funciona ordenando as arestas pelo menor peso e adicionando cada uma delas à solução, desde que essa aresta não forme ciclo. Para controlar isso, o programa usa a estrutura Union-Find.

Assim como no Dijkstra, o usuário pode escolher se a árvore será montada considerando distância, tempo ou custo.

## 6. Aplicação real

A aplicação construída é simples, mas representa uma ideia usada em sistemas reais. Aplicativos de mapas, sistemas de roteirização, redes sociais, plataformas de entrega e sistemas de telecomunicações usam grafos para representar conexões e calcular caminhos.

Em uma empresa de logística, por exemplo, algoritmos de caminho mínimo podem ajudar a encontrar rotas mais rápidas ou mais baratas para entregas. Já algoritmos de árvore geradora mínima podem apoiar decisões de conexão entre pontos, buscando reduzir custos de infraestrutura.

Um desafio que surgiria se o grafo crescesse muito seria o desempenho. Com milhares ou milhões de vértices e arestas, seria necessário usar estruturas mais otimizadas, bancos de dados especializados em grafos e estratégias para processar grandes volumes de dados. Além disso, em sistemas reais os pesos podem mudar com frequência, como trânsito, pedágios, combustível e disponibilidade de veículos.

## 7. Conclusão

O projeto mostra como uma situação real pode ser modelada como grafo e analisada com algoritmos clássicos. A lista de adjacência foi usada para armazenar o grafo de forma eficiente, a busca em largura permitiu verificar conectividade, o Dijkstra encontrou caminhos mínimos e o Kruskal gerou uma forma de conectar todos os pontos com menor custo total.
