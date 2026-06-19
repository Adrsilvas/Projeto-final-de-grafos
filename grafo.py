rom __future__ import annotations

import csv
import heapq
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Aresta:
    origem: str
    destino: str
    peso: float


class Grafo:
    """Grafo ponderado usando lista de adjacência."""

    def __init__(self, direcionado: bool = False) -> None:
        self.direcionado = direcionado
        self.adj: Dict[str, List[Tuple[str, float]]] = defaultdict(list)

    def adicionar_vertice(self, vertice: str) -> None:
        self.adj.setdefault(vertice, [])

    def adicionar_aresta(self, origem: str, destino: str, peso: float) -> None:
        if peso < 0:
            raise ValueError("Dijkstra não aceita pesos negativos.")

        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)

        self.adj[origem].append((destino, peso))

        if not self.direcionado:
            self.adj[destino].append((origem, peso))

    @classmethod
    def carregar_de_csv(cls, caminho_csv: str | Path, direcionado: bool = False) -> "Grafo":
        grafo = cls(direcionado=direcionado)
        caminho = Path(caminho_csv)

        with caminho.open("r", encoding="utf-8", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            colunas_obrigatorias = {"origem", "destino", "custo_km"}
            if not colunas_obrigatorias.issubset(leitor.fieldnames or []):
                raise ValueError("O CSV precisa ter as colunas: origem, destino e custo_km.")

            for linha in leitor:
                origem = linha["origem"].strip()
                destino = linha["destino"].strip()
                peso = float(linha["custo_km"])

                grafo.adicionar_aresta(origem, destino, peso)

        return grafo

    def vertices(self) -> List[str]:
        return sorted(self.adj.keys())

    def arestas(self) -> List[Aresta]:
        resultado: List[Aresta] = []
        vistas = set()

        for origem, vizinhos in self.adj.items():
            for destino, peso in vizinhos:
                if self.direcionado:
                    chave = (origem, destino)
                else:
                    chave = tuple(sorted((origem, destino)))

                if chave in vistas:
                    continue

                vistas.add(chave)
                resultado.append(Aresta(origem, destino, peso))

        return resultado

    def busca_em_largura(self, origem: str) -> Dict[str, int]:
        self._validar_vertice(origem)

        visitados = {origem: 0}
        fila = deque([origem])

        while fila:
            atual = fila.popleft()

            for vizinho, _ in self.adj[atual]:
                if vizinho not in visitados:
                    visitados[vizinho] = visitados[atual] + 1
                    fila.append(vizinho)

        return visitados

    def existe_caminho(self, origem: str, destino: str) -> bool:
        alcancaveis = self.busca_em_largura(origem)
        return destino in alcancaveis

    def dijkstra(self, origem: str, destino: str) -> Tuple[float, List[str]]:
        self._validar_vertice(origem)
        self._validar_vertice(destino)

        distancias = {vertice: float("inf") for vertice in self.adj}
        anteriores: Dict[str, str | None] = {vertice: None for vertice in self.adj}

        distancias[origem] = 0
        fila_prioridade: List[Tuple[float, str]] = [(0, origem)]

        while fila_prioridade:
            distancia_atual, atual = heapq.heappop(fila_prioridade)

            if distancia_atual > distancias[atual]:
                continue

            if atual == destino:
                break

            for vizinho, peso in self.adj[atual]:
                nova_distancia = distancia_atual + peso

                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

        if distancias[destino] == float("inf"):
            return float("inf"), []

        caminho = self._reconstruir_caminho(anteriores, destino)
        return distancias[destino], caminho

    def arvore_geradora_minima_prim(self, origem: str | None = None) -> Tuple[float, List[Aresta]]:
        if self.direcionado:
            raise ValueError("Prim deve ser usado em grafos não direcionados.")

        if not self.adj:
            return 0, []

        inicio = origem or next(iter(self.adj))
        self._validar_vertice(inicio)

        visitados = {inicio}
        fila_prioridade: List[Tuple[float, str, str]] = []
        resultado: List[Aresta] = []
        custo_total = 0.0

        for vizinho, peso in self.adj[inicio]:
            heapq.heappush(fila_prioridade, (peso, inicio, vizinho))

        while fila_prioridade and len(visitados) < len(self.adj):
            peso, origem_aresta, destino_aresta = heapq.heappop(fila_prioridade)

            if destino_aresta in visitados:
                continue

            visitados.add(destino_aresta)
            resultado.append(Aresta(origem_aresta, destino_aresta, peso))
            custo_total += peso

            for proximo, peso_proximo in self.adj[destino_aresta]:
                if proximo not in visitados:
                    heapq.heappush(fila_prioridade, (peso_proximo, destino_aresta, proximo))

        if len(visitados) < len(self.adj):
            raise ValueError("O grafo não é conectado, então não há árvore geradora mínima para todos os vértices.")

        return custo_total, resultado

    def _reconstruir_caminho(self, anteriores: Dict[str, str | None], destino: str) -> List[str]:
        caminho = []
        atual: str | None = destino

        while atual is not None:
            caminho.append(atual)
            atual = anteriores[atual]

        caminho.reverse()
        return caminho

    def _validar_vertice(self, vertice: str) -> None:
        if vertice not in self.adj:
            raise ValueError(f"Vértice não encontrado: {vertice}")
