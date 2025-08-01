import os.path

import app.config
from app.data_processing import converter_dados

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from tkinter import filedialog


class PopupConfirmacao(Popup):
    def confirmar(self):
        self.dismiss()
        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        converter_dados(caminho_arquivo)

class PopupAlterarDB(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.trocar_linha_tab)
        Window.bind(on_key_down=self.confirmar_config_enter)

    def trocar_linha_tab(self, window, key, scancode, codepoint, modifier):
        if key == 9:
            if self.ids.host.focus:
                self.ids.porta.focus = True
                return True
            elif self.ids.porta.focus:
                self.ids.user.focus = True
                return True
            elif self.ids.user.focus:
                self.ids.password.focus = True
                return True
            elif self.ids.password.focus:
                self.ids.database.focus = True
                return True
            elif self.ids.database.focus:
                self.ids.host.focus = True
                return True
        return False

    def confirmar_config_enter(self, window, key, scancode, codepoint, modifier):
        if key == 13:
            self.ids.confirmar_config.trigger_action()

    def salvar_configuracoes_db(self, host, porta, user, senha, base_dados):
        with open('init.env', 'w') as env:
            env.write(f'DB_HOST={host}\n')
            env.write(f'DB_PORT={porta}\n')
            env.write(f'DB_USER={user}\n')
            env.write(f'DB_PASSWORD={senha}\n')
            env.write(f'DB_BASEDADOS={base_dados}')
        self.dismiss()

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def cadastrar_db(self):
        PopupAlterarDB().open()

class TelaPrincipal(Screen):

    def selecionar_arquivo(self):
        return PopupConfirmacao().open()

class Aplicativo(App):

    def build(self):
        Builder.load_file("assets/UI/widgets.kv")
        return Builder.load_file("assets/UI/interface.kv")

if __name__ == '__main__':
    Aplicativo().run()
