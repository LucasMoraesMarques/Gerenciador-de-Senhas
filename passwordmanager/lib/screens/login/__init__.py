from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.clock import Clock
from lib.user import User
from lib.widgets import EnterPopup, RegisterPopupError
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.graphics import *
from datetime import datetime
from functools import partial

firstEntry = True


class LoginScreen(Screen):
    time = 300

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def enterUser(self, name, password):
        global firstEntry
        self.loading = Image(source='assets/media/loading.gif',
                             size_hint=(0.04, 0.04),
                             pos_hint={'x': 0.33, 'y': 0.39},
                             anim_delay=0.10)
        self.add_widget(self.loading)
        self.ids.enter.text = 'Autenticando credenciais ...'
        self.ids.enter.disabled = True
        user = User(name, password)
        if user.exist:
            user.authenticate()
            if user.authenticated:
                Clock.schedule_once(partial(self.showManager, user), 3)
                Clock.schedule_once(partial(self.resetScreen, self.ids.enter, 'Entrar', self.loading), 4)
                firstEntry = False
            else:
                popup = EnterPopup()
                Clock.schedule_once(popup.open, 3)
                Clock.schedule_once(partial(self.resetScreen, self.ids.enter, 'Entrar', self.loading), 4)
        else:
            popup = EnterPopup()
            popup.title = 'Usuário inexistente'
            popup.ids.container.children[0].children[1].text = 'Cadastre um usuário para poder gerenciar suas senhas'
            Clock.schedule_once(partial(self.resetScreen, self.ids.enter, 'Entrar', self.loading), 4)
            Clock.schedule_once(popup.open, 3)

    def createUser(self):
        box = BoxLayout(orientation='vertical')
        login = TextInput(multiline=False,
                          hint_text='Digite seu login',
                          size_hint=(1, 0.27))
        box.add_widget(login)
        psw1 = TextInput(multiline=False,
                         hint_text='Digite sua senha',
                         password=True,
                         size_hint=(1, 0.27))
        box.add_widget(psw1)
        psw2 = TextInput(multiline=False,
                         hint_text='Confirma a sua senha',
                         password=True,
                         size_hint=(1, 0.27))
        box.add_widget(psw2)
        btn = Button(text='Cadastrar',
                     on_press=partial(self.register, login, psw1, psw2),
                     size_hint=(1, 0.19),
                     font_size=20)
        box.add_widget(btn)
        popup = Popup(title='Cadastre um usuário',
                      content=box,
                      size_hint=(None, None),
                      size=(400, 300))
        btn.bind(on_release=popup.dismiss)

        popup.open()

    def register(self, login, psw1, psw2, btn):
        self.loading = Image(source='assets/media/loading.gif',
                             size_hint=(0.04, 0.04),
                             pos_hint={'x': 0.33, 'y': 0.30},
                             anim_delay=0.10)
        self.add_widget(self.loading)
        self.ids.register.text = 'Registrando credenciais ...'
        self.ids.register.disabled = True
        if login.text !='' and psw1.text != '' and psw2.text != '':
            if psw1.text == psw2.text:
                user = User(login.text, psw1.text)
                if not user.exist:
                    user.createDataBase()
                    user.insertUserCred()
                    user.authenticated = True
                    Clock.schedule_once(partial(self.showManager, user), 3)
                    Clock.schedule_once(partial(self.resetScreen, self.ids.register, 'Cadastre-se', self.loading), 4)
                else:
                    popup = RegisterPopupError()
                    Clock.schedule_once(partial(self.resetScreen, self.ids.register, 'Cadastre-se', self.loading), 2.5)
                    Clock.schedule_once(popup.open, 3)
            else:
                popup = RegisterPopupError()
                popup.title = 'Senhas incompatíveis'
                popup.ids.container.children[0].children[1].text = 'Tente novamente! Verifique se as senhas são iguais.'
                Clock.schedule_once(partial(self.resetScreen, self.ids.register, 'Cadastre-se', self.loading), 2.5)
                Clock.schedule_once(popup.open, 3)
        else:
            Clock.schedule_once(partial(self.resetScreen, self.ids.register, 'Cadastre-se', self.loading), 0.01)
            popup = RegisterPopupError()
            popup.title = 'Usuário com credenciais nulas'
            popup.ids.container.children[0].children[1].text = 'Não cadastre credenciais nulas. Pense em sua segurança!'
            popup.open()

    def showManager(self, user, *args):
        global firstEntry
        app = App.get_running_app()
        if not firstEntry:
            app.managerScreen.__init__()
            LoginScreen.time = 300
        self.ids.login.text = ''
        self.ids.psw.text = ''
        self.manager.transition.direction = 'left'
        self.manager.current = 'manager'
        self.clockStop = Clock.schedule_once(app.stop, 300)
        self.clockTime = Clock.schedule_interval(self.updateTime, 1)
        app.managerScreen.ids.session.text = 'Sessão iniciada em ' + datetime.now().strftime('%d/%m/%Y %H:%M')
        app.managerScreen.showData(user)

    def updateTime(self, dt):
        app = App.get_running_app()
        LoginScreen.time -= dt
        app.managerScreen.ids.time.text = f'{LoginScreen.time:.0f}' + ' segundos restantes'

    def resetScreen(self, btn, text, widget, dt):
        self.ids.login.text = ''
        self.ids.psw.text = ''
        btn.text = text
        btn.disabled = False
        self.remove_widget(widget)
