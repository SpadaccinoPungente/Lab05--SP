import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Lab O5 - segreteria studenti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._ddCorso = None
        self._btnCercaIscritti = None
        self._txtMatricola = None
        self._txtNome = None
        self._txtCognome = None
        self._btnCercaStudente = None
        self._btnCercaCorsi = None
        self._btnIscrivi = None
        self.txt_result = None


    def load_interface(self):
        self._title = ft.Text("App gestione studenti", color="blue", size=24)

        self._ddCorso = ft.Dropdown(label="Corso", hint_text="Selezionare un corso", width=500)
        self._controller.fillDDCorso()
        self._btnCercaIscritti = ft.ElevatedButton(text="Cerca Iscritti", on_click=self._controller.handleCercaIscritti)

        row1 = ft.Row([self._ddCorso, self._btnCercaIscritti], alignment=ft.MainAxisAlignment.CENTER)

        self._txtMatricola = ft.TextField(label="Matricola", width=200, hint_text="Inserire matricola")
        self._txtNome = ft.TextField(label="Nome", width=200, read_only=True)
        self._txtCognome = ft.TextField(label="Cognome", width=200, read_only=True)

        row2 = ft.Row([self._txtMatricola, self._txtNome, self._txtCognome], alignment=ft.MainAxisAlignment.CENTER)

        self._btnCercaStudente = ft.ElevatedButton(text="Cerca Studente", on_click=self._controller.handleCercaStudente)
        self._btnCercaCorsi = ft.ElevatedButton(text="Cerca Corsi", on_click=self._controller.handleCercaCorsi)
        self._btnIscrivi = ft.ElevatedButton(text="Iscrivi", on_click=self._controller.handleIscrivi)

        row3 = ft.Row([self._btnCercaStudente, self._btnCercaCorsi, self._btnIscrivi], alignment=ft.MainAxisAlignment.CENTER)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        self._page.controls.extend([self._title, row1, row2, row3, self.txt_result])
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        """Function that opens a popup alert window, displaying a message
        :param message: the message to be displayed"""
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
