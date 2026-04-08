import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def fill_dd_corsi(self):
        """Metodo da chiamare all'avvio dell'app per popolare i dati iniziali."""

        # Recupero gli oggetti Corso da model
        corsi = self._model.get_all_corsi()

        # Creo le opzioni per il dropdown
        for corso in corsi:
            # key: il valore 'nascosto' usato per le ricerche (codins)
            # text: il valore mostrato all'utente (sfruttiamo il metodo __str__ del DTO)
            opzione = ft.dropdown.Option(key=corso.codins, text=str(corso))
            self._view.dd_corso.options.append(opzione)

        self._view.update_page()

    def handle_cerca_iscritti(self, e):
        """Gestisce il click sul bottone 'Cerca iscritti'"""

        # Flet salva nella proprietà 'value' la 'key' dell'Option selezionata
        codins_corso = self._view.dd_corso.value

        # Controllo degli errori: se non è stato selezionato nulla, value è None
        if codins_corso is None:
            self._view.create_alert("Selezionare un corso!")
            return

        # UX CLEAR: svuoto i campi relativi allo studente singolo
        self._view.txt_matricola.value = ""
        self._view.txt_nome.value = ""
        self._view.txt_cognome.value = ""

        # Interrogo il Model passandogli il codice del corso
        iscritti = self._model.get_studenti_by_corso(codins_corso)

        # Pulisco la ListView dai risultati di eventuali ricerche precedenti
        self._view.lv_out.controls.clear()

        # Popolo la ListView con i risultati
        if len(iscritti) == 0:
            self._view.lv_out.controls.append(ft.Text("Nessun iscritto trovato per questo corso."))
        else:
            # Aggiungo la stringa iniziale con il conteggio, come da traccia (Punto 2)
            self._view.lv_out.controls.append(ft.Text(f"Ci sono {len(iscritti)} iscritti al corso:"))

            for studente in iscritti:
                self._view.lv_out.controls.append(ft.Text(f"{studente}")) # Sfrutto __str__ di Studente

        self._view.update_page()

    def handle_cerca_studente(self, e):
        """Gestisce il click sul bottone 'Cerca studente'"""
        matricola = self._view.txt_matricola.value

        if matricola == "":
            self._view.create_alert("Inserire una matricola!")
            return

        # Pulisco gli altri campi per coerenza visiva
        self._view.dd_corso.value = None
        self._view.lv_out.controls.clear()

        # Chiamo la funzione di supporto
        self._update_studente_in_view(matricola)

        self._view.update_page()

    def handle_cerca_corsi(self, e):
        """Gestisce il click sul bottone 'Cerca corsi'"""
        matricola = self._view.txt_matricola.value

        if matricola == "":
            self._view.create_alert("Inserire una matricola!")
            return

        # Pulisco gli altri campi
        self._view.dd_corso.value = None
        self._view.lv_out.controls.clear()

        # Chiamo la funzione di supporto e verifico il risultato
        studente_esiste = self._update_studente_in_view(matricola)

        if not studente_esiste:
            # Se lo studente non esiste, la funzione ha già mostrato un alert.
            # Io mi limito ad aggiornare la UI e fermare l'esecuzione.
            self._view.update_page()
            return

        # Se arrivo qui, lo studente esiste al 100%
        corsi = self._model.get_corsi_for_studente(matricola)

        if len(corsi) == 0:
            self._view.lv_out.controls.append(ft.Text("Questo studente non è iscritto a nessun corso."))
        else:
            self._view.lv_out.controls.append(ft.Text(f"Risultano {len(corsi)} corsi:"))
            for corso in corsi:
                self._view.lv_out.controls.append(ft.Text(f"{corso}"))

        self._view.update_page()

    def _update_studente_in_view(self, matricola: str) -> bool:
        """
        Cerca lo studente nel DB e popola i campi Nome e Cognome della View.
        Restituisce True se lo trova, False se non esiste.
        """
        studente = self._model.get_studente_by_matricola(matricola)

        if studente is None:
            self._view.create_alert(f"Nessuno studente trovato con matricola {matricola}.")
            self._view.txt_nome.value = ""
            self._view.txt_cognome.value = ""
            return False

        self._view.lv_out.controls.append(ft.Text(value=f"Studente trovato per matricola {matricola}.", color="green"))
        self._view.txt_nome.value = studente.nome
        self._view.txt_cognome.value = studente.cognome
        return True

    def handle_iscrivi(self, e):
        """Gestisce il click sul bottone 'Iscrivi'"""

        matricola = self._view.txt_matricola.value
        codins = self._view.dd_corso.value

        # Controlli preliminari sui campi di input
        if matricola == "":
            self._view.create_alert("Inserire una matricola!")
            return

        if codins is None:
            self._view.create_alert("Selezionare un corso dal menù a tendina!")
            return

        # Controllo se lo studente esiste nel DB (e intanto aggiorno Nome e Cognome)
        studente_esiste = self._update_studente_in_view(matricola)
        if not studente_esiste:
            # Se lo studente non esiste, _update_studente_in_view ha già mostrato un alert.
            self._view.update_page()
            return

        # Provo a effettuare l'iscrizione
        successo = self._model.iscrivi_studente(matricola, codins)

        # Aggiorno l'interfaccia dando un feedback all'utente
        self._view.lv_out.controls.clear()

        if successo:
            self._view.lv_out.controls.append(ft.Text(
                value=f"Iscrizione al corso {codins} avvenuta con successo!",
                color="green")
            )
        else:
            self._view.create_alert("Attenzione: questo studente risulta già iscritto a questo corso!")

        self._view.update_page()

"""
# VECCHIA VERSIONE: contiene handle_cerca_studente vecchia e handle_cerca_corsi che lo richiama
# NUOVA VERSIONE: metodo helper _update_studente_in_view

    def handle_cerca_studente(self, e):

        # Leggo la matricola inserita dall'utente
        matricola = self._view.txt_matricola.value

        # Controllo che l'utente non abbia lasciato il campo vuoto
        if matricola == "":
            self._view.create_alert("Inserire una matricola per cercare lo studente!")
            return

        # UX CLEAR: resetto il dropdown del corso e pulisco la ListView in basso
        self._view.dd_corso.value = None
        self._view.lv_out.controls.clear()

        # Interrogo il Model
        studente = self._model.get_studente_by_matricola(matricola)

        # Aggiorno l'interfaccia
        if studente is None:
            # Lo studente non esiste: mostro avviso e pulisco eventuali dati vecchi nei campi
            self._view.create_alert(f"Nessuno studente trovato con matricola {matricola}.")
            self._view.txt_nome.value = ""
            self._view.txt_cognome.value = ""
        else:
            # Lo studente esiste: compilo i campi di testo con nome e cognome
            self._view.lv_out.controls.append(ft.Text(value=f"Studente trovato per matricola {matricola}.", color="green"))
            self._view.txt_nome.value = studente.nome
            self._view.txt_cognome.value = studente.cognome

        self._view.update_page()

    def handle_cerca_corsi(self, e):

        # Riciclo il lavoro fatto dall'altro bottone
        # Questo popolerà i campi di testo o mostrerà alert di errore
        self.handle_cerca_studente(e)

        # Come faccio a sapere se lo studente è stato trovato? Controllo se l'altro metodo ha compilato il nome.
        # Se è vuoto, significa che lo studente non esiste (o la matricola era vuota).
        if self._view.txt_nome.value == "":
            return  # Mi fermo qui -> alert di errore è già stato mostrato dall'altro metodo

        # Se arrivo qui, lo studente esiste al 100% e i campi di testo sono compilati.
        matricola = self._view.txt_matricola.value

        # Chiedo i corsi a Model
        corsi = self._model.get_corsi_for_studente(matricola)

        # Popolo la ListView
        # Nota: handle_cerca_studente ha già fatto self._view.lv_out.controls.clear()
        if len(corsi) == 0:
            self._view.lv_out.controls.append(ft.Text("Questo studente non è iscritto a nessun corso."))
        else:
            self._view.lv_out.controls.append(ft.Text(f"Risultano {len(corsi)} corsi:"))
            for corso in corsi: self._view.lv_out.controls.append(ft.Text(f"{corso}"))

        self._view.update_page()
"""
