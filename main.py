import csv
import heapq
from collections import deque
from pathlib import Path


class GrafoLogistico:
    """
    Grafo não direcionado e ponderado.
    Vértices: cidades / pontos logísticos.
    Arestas: rotas entre cidades.
    Pesos: distância, tempo e custo.
    """

    def __init__(self):
        self.adjacencia = {}

    def adicionar_vertice(self, vertice):
        if vertice not in self.adjacencia:
            self.adjacencia[vertice] = []

    def adicionar_aresta(self, origem, destino, distancia_km, tempo_min, custo_reais):
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)

        rota = {
            "destino": destino,
            "distancia_km": float(distancia_km),
            "tempo_min": float(tempo_min),
            "custo_reais": float(custo_reais)
        }

        rota_volta = {
            "destino": origem,
            "distancia_km": float(distancia_km),
            "tempo_min": float(tempo_min),
            "custo_reais": float(custo_reais)
        }

        self.adjacencia[origem].append(rota)
        self.adjacencia[destino].append(rota_volta)

    @classmethod
    def carregar_csv(cls, caminho_csv):
        grafo = cls()

        with open(caminho_csv, "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)

            for linha in leitor:
                grafo.adicionar_aresta(
                    linha["origem"],
                    linha["destino"],
                    linha["distancia_km"],
                    linha["tempo_min"],
                    linha["custo_reais"]
                )

        return grafo

    def vertices(self):
        return list(self.adjacencia.keys())

    def mostrar_grafo(self):
        print("\nGRAFO CARREGADO")
        print("-" * 60)

        for cidade, rotas in self.adjacencia.items():
            conexoes = []
            for rota in rotas:
                conexoes.append(
                    f"{rota['destino']} "
                    f"({rota['distancia_km']:.0f} km, "
                    f"{rota['tempo_min']:.0f} min, "
                    f"R$ {rota['custo_reais']:.2f})"
                )
            print(f"{cidade}: {', '.join(conexoes)}")

    def busca_largura(self, origem):
        if origem not in self.adjacencia:
            raise ValueError(f"Origem '{origem}' não existe no grafo.")

        visitados = set()
        ordem = []
        fila = deque([origem])
        visitados.add(origem)

        while fila:
            atual = fila.popleft()
            ordem.append(atual)

            for rota in self.adjacencia[atual]:
                vizinho = rota["destino"]
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        return ordem

    def existe_caminho(self, origem, destino):
        if origem not in self.adjacencia or destino not in self.adjacencia:
            return False

        visitados = set()
        fila = deque([origem])
        visitados.add(origem)

        while fila:
            atual = fila.popleft()

            if atual == destino:
                return True

            for rota in self.adjacencia[atual]:
                vizinho = rota["destino"]
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    fila.append(vizinho)

        return False

    def dijkstra(self, origem, destino, peso="distancia_km"):
        """
        Encontra o menor caminho considerando o campo informado em peso.
        Opções: distancia_km, tempo_min ou custo_reais.
        """
        if origem not in self.adjacencia:
            raise ValueError(f"Origem '{origem}' não existe no grafo.")
        if destino not in self.adjacencia:
            raise ValueError(f"Destino '{destino}' não existe no grafo.")

        distancias = {vertice: float("inf") for vertice in self.adjacencia}
        anteriores = {vertice: None for vertice in self.adjacencia}
        distancias[origem] = 0

        fila_prioridade = [(0, origem)]

        while fila_prioridade:
            custo_atual, atual = heapq.heappop(fila_prioridade)

            if custo_atual > distancias[atual]:
                continue

            if atual == destino:
                break

            for rota in self.adjacencia[atual]:
                vizinho = rota["destino"]
                novo_custo = custo_atual + rota[peso]

                if novo_custo < distancias[vizinho]:
                    distancias[vizinho] = novo_custo
                    anteriores[vizinho] = atual
                    heapq.heappush(fila_prioridade, (novo_custo, vizinho))

        if distancias[destino] == float("inf"):
            return None, float("inf")

        caminho = []
        atual = destino

        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]

        caminho.reverse()
        return caminho, distancias[destino]

    def kruskal(self, peso="distancia_km"):
        """
        Gera uma Árvore Geradora Mínima usando Kruskal.
        Como o grafo é não direcionado, remove duplicidades de arestas.
        """
        pai = {}
        rank = {}

        def encontrar(x):
            if pai[x] != x:
                pai[x] = encontrar(pai[x])
            return pai[x]

        def unir(x, y):
            raiz_x = encontrar(x)
            raiz_y = encontrar(y)

            if raiz_x == raiz_y:
                return False

            if rank[raiz_x] < rank[raiz_y]:
                pai[raiz_x] = raiz_y
            elif rank[raiz_x] > rank[raiz_y]:
                pai[raiz_y] = raiz_x
            else:
                pai[raiz_y] = raiz_x
                rank[raiz_x] += 1

            return True

        for vertice in self.adjacencia:
            pai[vertice] = vertice
            rank[vertice] = 0

        arestas = []
        vistas = set()

        for origem, rotas in self.adjacencia.items():
            for rota in rotas:
                destino = rota["destino"]
                chave = tuple(sorted([origem, destino]))

                if chave not in vistas:
                    vistas.add(chave)
                    arestas.append((rota[peso], origem, destino))

        arestas.sort()

        arvore = []
        custo_total = 0

        for custo, origem, destino in arestas:
            if unir(origem, destino):
                arvore.append((origem, destino, custo))
                custo_total += custo

        return arvore, custo_total


def imprimir_menu():
    print("\n" + "=" * 60)
    print("SISTEMA DE ROTAS LOGÍSTICAS COM GRAFOS")
    print("=" * 60)
    print("1 - Mostrar grafo")
    print("2 - Busca em largura a partir de uma cidade")
    print("3 - Verificar se existe caminho entre duas cidades")
    print("4 - Menor caminho com Dijkstra")
    print("5 - Árvore Geradora Mínima com Kruskal")
    print("0 - Sair")


def escolher_peso():
    print("\nEscolha o peso:")
    print("1 - Distância em km")
    print("2 - Tempo em minutos")
    print("3 - Custo em reais")

    opcao = input("Opção: ").strip()

    if opcao == "2":
        return "tempo_min", "min"
    if opcao == "3":
        return "custo_reais", "reais"

    return "distancia_km", "km"


def main():
    caminho_csv = Path(__file__).resolve().parent.parent / "data" / "rotas.csv"
    grafo = GrafoLogistico.carregar_csv(caminho_csv)

    while True:
        imprimir_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                grafo.mostrar_grafo()

            elif opcao == "2":
                origem = input("Cidade de origem: ").strip()
                ordem = grafo.busca_largura(origem)
                print("\nCidades alcançáveis a partir de", origem)
                print(" -> ".join(ordem))

            elif opcao == "3":
                origem = input("Cidade de origem: ").strip()
                destino = input("Cidade de destino: ").strip()

                if grafo.existe_caminho(origem, destino):
                    print(f"\nExiste caminho entre {origem} e {destino}.")
                else:
                    print(f"\nNão existe caminho entre {origem} e {destino}.")

            elif opcao == "4":
                origem = input("Cidade de origem: ").strip()
                destino = input("Cidade de destino: ").strip()
                peso, unidade = escolher_peso()

                caminho, custo = grafo.dijkstra(origem, destino, peso)

                if caminho is None:
                    print("\nNão foi encontrado caminho.")
                else:
                    print("\nMenor caminho encontrado:")
                    print(" -> ".join(caminho))
                    if unidade == "reais":
                        print(f"Custo total: R$ {custo:.2f}")
                    else:
                        print(f"Custo total: {custo:.0f} {unidade}")

            elif opcao == "5":
                peso, unidade = escolher_peso()
                arvore, custo_total = grafo.kruskal(peso)

                print("\nÁrvore Geradora Mínima:")
                for origem, destino, custo in arvore:
                    if unidade == "reais":
                        print(f"{origem} - {destino}: R$ {custo:.2f}")
                    else:
                        print(f"{origem} - {destino}: {custo:.0f} {unidade}")

                if unidade == "reais":
                    print(f"\nCusto total da árvore: R$ {custo_total:.2f}")
                else:
                    print(f"\nCusto total da árvore: {custo_total:.0f} {unidade}")

            elif opcao == "0":
                print("Encerrando o programa.")
                break

            else:
                print("Opção inválida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
