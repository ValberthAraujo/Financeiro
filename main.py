import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'

from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, SlideTransition, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder
from tkinter import filedialog
from app.conversores.csv import converter_dados


class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Arquivo Excel", "*.xlsx")]
        )

        converter_dados(caminho_arquivo)

class TelaPrincipal(Screen):
    pass

Builder.load_file("./assets/UI/interface.kv")

class Aplicativo(App):

    def build(self):
        return Builder.load_file("./assets/UI/interface.kv")

    @staticmethod
    def show_popup():
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text="Seleção cancelada"))
        btn = Button(text="Fechar", size_hint_y=None, height=40)
        content.add_widget(btn)

        popup = Popup(title="Aviso",
                      content=content,
                      size_hint=(None, None),
                      size=(300, 200),
                      auto_dismiss=False)

        btn.bind(on_release=popup.dismiss)  # Fecha o popup ao clicar no botão
        popup.open()

if __name__ == '__main__':
    Aplicativo().run()
