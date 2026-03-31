import flet as ft

from model.model import Model
from UI.view import View
from UI.controller import Controller


def main(page: ft.Page):
    lab5_model = Model()
    lab5_view = View(page)
    lab5_controller = Controller(lab5_view, lab5_model)
    lab5_view.controller = lab5_controller # lo faccio utilizzando il setter invece che set_connection()

    # chiamata a load_interface()
    lab5_view.load_interface()


ft.app(target=main)
