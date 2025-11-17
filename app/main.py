import os
import sys
from pathlib import Path

os.environ["KIVY_NO_ARGS"] = "1"
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_AUDIO"] = "sdl2"
os.environ["KIVY_VIDEO"] = "null"
os.environ["KIVY_GSTREAMER"] = "0"
os.environ["KIVY_CLOCK"] = "interrupt"
os.environ["KIVY_IMAGE"] = "sdl2"
os.environ["KIVY_WINDOW"] = "sdl2"
os.environ["KIVY_TEXT"] = "sdl2"
os.environ["KIVY_METRICS_DENSITY"] = "1"


from app.controller.data_processing import processar_extrato

from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.resources import resource_add_path

from tkinter import Tk, filedialog

from app.model.database_manager import criar_conexao


class PopupErro(Popup):
    pass


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESOURCE_ROOT = Path(getattr(sys, "_MEIPASS", PROJECT_ROOT))
VIEW_DIR = RESOURCE_ROOT / "app" / "view"
ASSETS_DIR = RESOURCE_ROOT / "assets"
CONFIG_DIR = Path.home() / ".controle_financeiro"
USER_ENV_FILE = CONFIG_DIR / "init.env"
DEFAULT_ENV_FILE = RESOURCE_ROOT / "init.env"


def resource_path(*parts: str) -> str:
    """Build absolute paths that also work once packaged."""
    return str(RESOURCE_ROOT.joinpath(*parts))


def ensure_resource_paths():
    for directory in {RESOURCE_ROOT, RESOURCE_ROOT / "app", VIEW_DIR, ASSETS_DIR}:
        if directory.exists():
            resource_add_path(str(directory))


def get_env_file() -> Path:
    if USER_ENV_FILE.exists():
        return USER_ENV_FILE
    if DEFAULT_ENV_FILE.exists():
        return DEFAULT_ENV_FILE
    return USER_ENV_FILE


ensure_resource_paths()


def _ask_pdf_file() -> str:
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return filedialog.askopenfilename(
            title="Selecione um arquivo PDF",
            filetypes=[("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")]
        )
    finally:
        root.destroy()


class PopupConfirmacao(Popup):
    def confirmar(self):
        caminho_arquivo = _ask_pdf_file()

        if not caminho_arquivo:
            PopupErro().open()
            return

        env_path = get_env_file()
        if not env_path.exists():
            PopupErro().open()
            return

        try:
            processar_extrato(caminho_arquivo, "VALBERTH")
            criar_conexao(str(env_path))
        except Exception:
            PopupErro().open()
        finally:
            self.dismiss()


class PopupAlterarDB(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.trocar_linha_tab)
        self.bind(on_dismiss=self._unbind_events)

    def _unbind_events(self, *_):
        Window.unbind(on_key_down=self.trocar_linha_tab)

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
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        with open(USER_ENV_FILE, 'w', encoding='utf-8') as env:
            env.write(f'DB_HOST={host}\n')
            env.write(f'DB_PORT={porta}\n')
            env.write(f'DB_USER={user}\n')
            env.write(f'DB_PASSWORD={senha}\n')
            env.write(f'DB_BASEDADOS={base_dados}')
        self.dismiss()

class TelaInicial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def cadastrar_db():
        PopupAlterarDB().open()

class TelaPrincipal(Screen):

    @staticmethod
    def selecionar_arquivo():
        return PopupConfirmacao().open()

class Aplicativo(App):
    icon = resource_path("assets", "icon.png")

    def build(self):
        Builder.load_file(resource_path("app", "view", "widgets.kv"))
        return Builder.load_file(resource_path("app", "view", "interface.kv"))

if __name__ == '__main__':
    Aplicativo().run()
