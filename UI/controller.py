import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fillDDCorso(self):
        self._view._ddCorso.options = [
            ft.dropdown.Option(key=c.codins, text=c) for c in self._model.getAllCorsi()
        ]

    def handleCercaIscritti(self, e):
        if self._view._ddCorso.value is None:
            self._view.create_alert("Selezionare un corso!")
            return
        iscritti = self._model.getIscrittiByCorso(self._view._ddCorso.value)
        self._view.txt_result.controls.clear()
        if len(iscritti) == 0:
            self._view.txt_result.controls.append(ft.Text("Non ci sono iscritti al corso"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Ci sono {len(iscritti)} iscritti al corso:"))
            for studente in iscritti: self._view.txt_result.controls.append(ft.Text(f"{studente}"))
        self._view.update_page()

    def handleCercaStudente(self, e):
        if self._view._txtMatricola.value == "":
            self._view.create_alert("Inserire una matricola!")
            return
        try: matr_int = int(self._view._txtMatricola.value)
        except ValueError:
            self._view.create_alert("Inserire una matricola valida!")
            return
        studente = self._model.getStudente(matr_int)
        if studente is None:
            self._view.create_alert("Matricola non trovata!")
            return
        self._view._txtNome.value = f"{studente.nome}"
        self._view._txtCognome.value = f"{studente.cognome}"
        self._view.update_page()

    def handleCercaCorsi(self, e):
        if self._view._txtMatricola.value == "":
            self._view.create_alert("Inserire una matricola!")
            return
        try: matr_int = int(self._view._txtMatricola.value)
        except ValueError:
            self._view.create_alert("Inserire una matricola valida!")
            return
        studente = self._model.getStudente(matr_int)
        if studente is None:
            self._view.create_alert("Matricola non trovata!")
            return
        corsi = self._model.getCorsiByMatricola(matr_int)
        if not corsi:
            self._view.txt_result.controls.append(ft.Text("Nessun corso trovato."))
            return
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Risultano {len(corsi)} corsi:"))
        for c in corsi: self._view.txt_result.controls.append(ft.Text(f"{c}"))

    def handleIscrivi(self, e):
        pass

