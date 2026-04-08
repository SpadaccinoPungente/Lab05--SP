import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):

        super().__init__() # da capire meglio, inizializza il padre di View <- UserControl

        # impostazioni generali della pagina
        self._page = page
        self._page.title = "Lab 05 - Database iscritti-corsi"  # Titolo della finestra aggiornato
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK

        # controller inizializzato nel main
        self._controller = None

        # dichiarazione elementi grafici (da istanziare dopo)
        self._title = None
        self.dd_corso = None  # dropdown per selezionare il corso
        self.btn_cerca_iscritti = None  # Bottone per cercare gli iscritti al corso

        self.txt_matricola = None  # Campo di testo editabile per la matricola
        self.txt_nome = None  # Campo di testo (sola lettura) per il nome
        self.txt_cognome = None  # Campo di testo (sola lettura) per il cognome

        self.btn_cerca_studente = None  # Bottone per cercare i dati dello studente
        self.btn_cerca_corsi = None  # Bottone per cercare i corsi a cui è iscritto
        self.btn_iscrivi = None  # Bottone per iscrivere lo studente

        self.lv_out = None  # ListView per mostrare i risultati in basso

    def load_interface(self):
        """Funzione che carica gli elementi grafici della vista (View)"""

        # titolo dell'applicazione
        self._title = ft.Text("App Gestione Studenti", color="blue", size=24)
        self._page.controls.append(self._title)

        # RIGA 1: dropdown corsi, bottone "Cerca iscritti"
        self.dd_corso = ft.Dropdown(
            label="Corso",
            hint_text="Selezionare un corso",
            width=500,
            options=[] # opzioni caricate dal Controller!
        )

        self.btn_cerca_iscritti = ft.ElevatedButton(
            text="Cerca iscritti",
            on_click=self._controller.handle_cerca_iscritti
        )

        # creazione row1
        row1 = ft.Row(
            controls=[self.dd_corso, self.btn_cerca_iscritti],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # RIGA 2: campi di testo per Matricola, Nome, Cognome
        self.txt_matricola = ft.TextField(label="matricola", width=150)
        self.txt_nome = ft.TextField(label="nome", width=250, read_only=True) # read_only
        self.txt_cognome = ft.TextField(label="cognome", width=250, read_only=True) # read_only

        # creazione row2
        row2 = ft.Row(
            controls=[self.txt_matricola, self.txt_nome, self.txt_cognome],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # TERZA RIGA: bottoni per la gestione dello studente
        self.btn_cerca_studente = ft.ElevatedButton(
            text="Cerca studente",
            on_click=self._controller.handle_cerca_studente # da definire nel Controller
        )
        self.btn_cerca_corsi = ft.ElevatedButton(
            text="Cerca corsi",
            on_click=self._controller.handle_cerca_corsi # da definire nel Controller
        )
        self.btn_iscrivi = ft.ElevatedButton(
            text="Iscrivi",
            on_click=self._controller.handle_iscrivi # da definire nel Controller
        )

        # creazione row3
        row3 = ft.Row(
            controls=[self.btn_cerca_studente, self.btn_cerca_corsi, self.btn_iscrivi],
            alignment=ft.MainAxisAlignment.CENTER
        )

        # listview
        self.lv_out = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # inserisco le righe in _page.controls
        self._page.controls.extend([row1, row2, row3, self.lv_out])

        # popolo il dropdown (avrebbe più senso chiamare il controller nel main)
        self._controller.startup()

        # da non dimenticare mai
        self._page.update()

    # getter e setter
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    # utilità
    def create_alert(self, message):
        """Funzione per aprire una finestra di dialogo pop-up di avviso"""
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg # attributo definito qui, non in __init__
        dlg.open = True
        self._page.update()

    def update_page(self):
        """Aggiorna il rendering della pagina"""
        self._page.update()
