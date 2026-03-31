import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def startup(self):
        """
        Metodo da chiamare all'avvio dell'app per popolare i dati iniziali.
        Qui chiederemo a model di leggere i corsi dal database e li
        inseriremo nel Dropdown della View.
        """
        pass

    def handle_cerca_iscritti(self, e):
        """Gestisce il click sul bottone 'Cerca iscritti'"""
        pass

    def handle_cerca_studente(self, e):
        """Gestisce il click sul bottone 'Cerca studente'"""
        pass

    def handle_cerca_corsi(self, e):
        """Gestisce il click sul bottone 'Cerca corsi'"""
        pass

    def handle_iscrivi(self, e):
        """Gestisce il click sul bottone 'Iscrivi'"""
        pass

"""
    def handle_hello(self, e): # esempio
        name = self._view.txt_name.value
        if name is None or name == "":
            self._view.create_alert("Inserire il nome")
            return
        self._view.txt_result.controls.append(ft.Text(f"Hello, {name}!"))
        self._view.update_page()
"""
