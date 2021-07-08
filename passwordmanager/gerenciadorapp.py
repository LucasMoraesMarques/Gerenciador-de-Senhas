from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.config import Config
from lib.screens.login import LoginScreen
from lib.screens.manager import ManagerScreen
# Configurando a GUI
Config.set('graphics', 'resizable', '0')
Config.write()
Config.set('graphics', 'width', '900')
Config.write()
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.write()

# Carregando arquivo de design


# Definindo a classe do app
class Gerenciador(App):
    icon = 'assets/media/shield-lock-fill.ico'

    def build(self):
        # Criando o gerenciador de telas
        self.screenManager = ScreenManager()

        # Tela de Login
        self.loginScreen = LoginScreen(name='login')
        self.screenManager.add_widget(self.loginScreen)

        # Tela de gerenciamento de senhas
        self.managerScreen = ManagerScreen(name='manager')
        self.screenManager.add_widget(self.managerScreen)

        return self.screenManager
