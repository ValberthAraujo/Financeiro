import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from tkinter import filedialog
from app.data_processing import converter_dados


class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Arquivo Excel", "*.xlsx")]
        )

        converter_dados(caminho_arquivo)

class PopupConfirmar(Popup):
    pass

class TelaPrincipal(Screen):
    pass

class Aplicativo(App):

    def build(self):
        Builder.load_file("./assets/ui/widgets.kv")
        return Builder.load_file("assets/UI/interface.kv")

    def show_confirmation(self):
        popup = PopupConfirmar()
        popup.open()

if __name__ == '__main__':
    Aplicativo().run()
