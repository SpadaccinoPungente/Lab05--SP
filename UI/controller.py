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
        # Pulire sempre i campi anagrafici e i vecchi risultati prima di iniziare
        self._view._txtNome.value = ""
        self._view._txtCognome.value = ""
        self._view.txt_result.controls.clear()

        if self._view._ddCorso.value is None:
            self._view.create_alert("Selezionare un corso!")
            self._view.update_page()
            return

        iscritti = self._model.getIscrittiByCorso(self._view._ddCorso.value)

        if len(iscritti) == 0:
            self._view.txt_result.controls.append(ft.Text("Non ci sono iscritti al corso"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Ci sono {len(iscritti)} iscritti al corso:"))
            for studente in iscritti:
                self._view.txt_result.controls.append(ft.Text(f"{studente}"))

        self._view.update_page()

    def handleCercaStudente(self, e):
        self._view._txtNome.value = ""
        self._view._txtCognome.value = ""
        self._view.txt_result.controls.clear()

        if self._view._txtMatricola.value == "":
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        try:
            matr_int = int(self._view._txtMatricola.value)
        except ValueError:
            self._view.create_alert("Inserire una matricola valida!")
            self._view.update_page()
            return

        studente = self._model.getStudente(matr_int)
        if studente is None:
            self._view.create_alert("Matricola non trovata!")
            self._view.update_page()
            return

        self._view._txtNome.value = f"{studente.nome}"
        self._view._txtCognome.value = f"{studente.cognome}"
        self._view.update_page()

    def handleCercaCorsi(self, e):
        self._view.txt_result.controls.clear()
        self._view._txtNome.value = ""
        self._view._txtCognome.value = ""

        if self._view._txtMatricola.value == "":
            self._view.create_alert("Inserire una matricola!")
            self._view.update_page()
            return
        try:
            matr_int = int(self._view._txtMatricola.value)
        except ValueError:
            self._view.create_alert("Inserire una matricola valida!")
            self._view.update_page()
            return

        studente = self._model.getStudente(matr_int)
        if studente is None:
            self._view.create_alert("Matricola non trovata!")
            self._view.update_page()
            return

        self._view._txtNome.value = f"{studente.nome}"
        self._view._txtCognome.value = f"{studente.cognome}"

        corsi = self._model.getCorsiByMatricola(matr_int)

        if not corsi:
            self._view.txt_result.controls.append(ft.Text("Nessun corso trovato."))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Risultano {len(corsi)} corsi:"))
            for c in corsi:
                self._view.txt_result.controls.append(ft.Text(f"{c}"))
        self._view.update_page()

    def handleIscrivi(self, e):
        if self._view._ddCorso.value is None:
            self._view.create_alert("Selezionare un corso prima di iscrivere!")
            return

        if self._view._txtMatricola.value == "":
            self._view.create_alert("Inserire una matricola!")
            return
        try:
            matr_int = int(self._view._txtMatricola.value)
        except ValueError:
            self._view.create_alert("Inserire una matricola valida!")
            return

        studente = self._model.getStudente(matr_int)
        if studente is None:
            self._view.create_alert("Impossibile iscrivere: matricola inesistente!")
            return

        # Recuperiamo il codice del corso dal Dropdown
        codins = self._view._ddCorso.value
        inserito = self._model.iscriviStudente(matr_int, codins)

        self._view.txt_result.controls.clear()
        if inserito:
            self._view.txt_result.controls.extend([
                ft.Text("Studente iscritto con successo al corso!"),
                ft.Text(f"Iscrizione completata: {studente.nome} {studente.cognome} è ora iscritto al corso {codins}.")])
        else:
            self._view.create_alert("Errore: Lo studente potrebbe essere già iscritto a questo corso.")

        self._view.update_page()