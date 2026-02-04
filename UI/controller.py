import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self.ruoli=[]
        self.ruolo_selezionato=None

        self.artisti=[]
        self.artista_selezionato=None
        self.id_map={}


    def handle_crea_grafo(self, e):
        if self.ruolo_selezionato is None:
            self._view.show_alert("prima è necessario selezionare un ruolo")
            return
        self._model.build_graph(self.ruolo_selezionato)
        n_nodi=self._model.get_num_nodes()
        n_archi=self._model.get_num_edges()
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Nodi: {n_nodi} | Archi: {n_archi}"))
        self._view.btn_classifica.disabled = False
        self._view.update()

    def handle_classifica(self, e):
        best_artisti=self._model.classifica()
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"artisti in ordine decrescente di influenza"))
        for a,p in best_artisti:
            self._view.list_risultato.controls.append(ft.Text(f" {a}  Delta={p}"))

        self._view.dd_iniziale.disabled = False
        self._view.btn_cerca_percorso.disabled = False
        self._view.dd_iniziale.clean()
        self.popola_dd_artista()
        self._view.update()


    def popola_dd_ruoli(self):
        self.ruoli= self._model.get_ruoli()
        for r in self.ruoli:
            self._view.dd_ruolo.options.append(ft.dropdown.Option(text=r))
        self._view.update()


    def gestisci_ruoli(self, e):
        """ Handler per gestire la selezione del ruolo dal dropdown"""
        valore = e.control.value
        self.ruolo_selezionato = valore

    def popola_dd_artista(self):
        self.artisti=[]
        self.artisti = self._model.get_nodi()
        for a in self.artisti:
            self._view.dd_iniziale.options.append(ft.dropdown.Option(key=a.artist_id, text=a.name))
        self._view.update()


    def gestisci_artisti(self, e):
        """ Handler per gestire la selezione dell'artista dal dropdown """""
        valore = e.control.value
        self.id_map = self._model.get_id_map()
        valore = int(valore)
        self.artista_selezionato = self.id_map[valore]

    def get_cammino(self,e):
        if self.artista_selezionato is None:
            self._view.show_alert("prima è necessario selezionare un artista iniziale")
            return
        L=self._view.input_L.value
        try:
            L=int(L)
        except:
            self._view.show_alert("inserire un valore intero valido")
            return
        if L<3 or L>len(self.artisti):
            self._view.show_alert(f"inserire un valore compreso tra 3 e {len(self.artisti)} ")
            return
        best_cammino,peso=self._model.get_cammino(self.artista_selezionato,L)
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Percorso ottimo"))

        print(best_cammino)
        for n in best_cammino:

            self._view.list_risultato.controls.append(ft.Text(f"{n}"))

        self._view.list_risultato.controls.append(ft.Text(f"peso totale={peso}"))
        self._view.update()


