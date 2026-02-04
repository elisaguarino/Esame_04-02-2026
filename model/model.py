import copy

import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.artisti = []
        self.id_map={}
        self.relazioni = []
        self.ruoli=[]
        self.artisti_ruolo=[]

        self.G=nx.DiGraph()
        self.nodes=[]
        self.edges=[]

    def build_graph(self, role: str):
        self.G.clear()
        self.nodes = []
        self.edges = []

        self.artisti=DAO.get_all_artisti()
        for a in self.artisti:
            self.id_map[a.artist_id]=a

        self.artisti_ruolo=DAO.get_artisti_ruoli(role)
        for a in self.artisti_ruolo:
            h=self.id_map[a]
            self.nodes.append(h)

        self.relazioni=DAO.get_edge(role)
        for i in range(len(self.relazioni)):
            for j in range(i + 1, len(self.relazioni)):
                id1, w1 = self.relazioni[i]
                id2, w2 = self.relazioni[j]

                p1 = self.id_map[id1]
                p2 = self.id_map[id2]
                peso =abs(float(w1) - float(w2))

                if w1 > w2:
                    # Da chi ha venduto di più a chi ha venduto di meno
                    self.G.add_edge(p1, p2, weight=peso)
                elif w2 > w1:
                    self.G.add_edge(p2, p1, weight=peso)
        print(self.G)

    def get_num_nodes(self):
        return self.G.number_of_nodes()
    def get_num_edges(self):
        return self.G.number_of_edges()

    def classifica(self):
        best_artisti = []
        for n in self.G.nodes:
            delta = 0
            for e_out in self.G.out_edges(n, data=True):
                delta += e_out[2]["weight"]
            for e_in in self.G.in_edges(n, data=True):
                delta -= e_in[2]["weight"]

            best_artisti.append((n, delta))

        best_artisti.sort(reverse=False, key=lambda x: x[1])
        return best_artisti

    def get_ruoli(self):
        self.ruoli=DAO.get_ruoli()
        return self.ruoli

    def get_nodi(self):
        return self.G.nodes()

    def get_id_map(self):
        return self.id_map

    def get_cammino(self,start,L):
        self.best_cammino=[]
        self.best_peso=float("-inf")

        partial=[start]
        self.ricorsione(partial,0.0,L)
        return self.best_cammino,self.best_peso

    def ricorsione(self,partial,peso,L):
        if len(partial) == L:
            if peso>self.best_peso:
                self.best_peso=peso
                self.best_cammino=copy.deepcopy(partial)
        n_last=partial[-1]
        for n in self.G.successors(n_last):
            if n not in partial:
                edge_data = self.G.get_edge_data(n_last, n)
                if edge_data is not None:
                    peso_arco = edge_data['weight']
                    partial.append(n)
                    self.ricorsione(partial,peso+peso_arco,L)
                    partial.pop()