import os
import time

from app.controller.data_processing import processar_extrato

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

from tkinter import filedialog

from app.model.database_manager import criar_conexao


class PopupErro(Popup):
    pass

class PopupConfirmacao(Popup):
    def confirmar(self):

        caminho_arquivo = filedialog.askopenfilename(
            title="Selecione um arquivo",
            filetypes=[("Todos os arquivos", "*.*")]
        )

        if caminho_arquivo != '':
            dados = processar_extrato(caminho_arquivo, "VALBERTH")
            conexao = criar_conexao(os.getcwd())
        else:
            PopupErro().open()


class PopupAlterarDB(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.trocar_linha_tab)

    def trocar_linha_tab(self, _, key, *__):
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

    def salvar_configuracoes_db(self, host, porta, user, senha, base_dados):
        env_path = os.path.join(os.getcwd(), "init.env")

        with open(env_path, 'w') as env:
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
        Builder.load_file("view/widgets.kv")
        return Builder.load_file("view/interface.kv")

if __name__ == '__main__':
    Aplicativo().run()
