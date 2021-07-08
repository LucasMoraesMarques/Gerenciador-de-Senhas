from kivy.app import App
from kivy.uix.screenmanager import Screen
from lib.widgets import Account, Login, Password, Check
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ManagerScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createForm(self):
        box = BoxLayout(orientation='vertical')
        self.acc = Account(readonly=False, size_hint=(1, 0.25))
        self.login = Login(readonly=False, size_hint=(1, 0.25))
        self.psw = Password(readonly=False, size_hint=(1, 0.25))
        box.add_widget(self.acc)
        box.add_widget(self.login)
        box.add_widget(self.psw)
        return box

    def showData(self, user):
        self.user = user
        self.ids.username.text = f'Bem-vindo(a), {user.name.capitalize()}'
        self.updateGrid()

    def updateGrid(self):
        rows = self.user.readData()
        self.grid = self.ids.grid
        self.grid.clear_widgets()
        self.rows = []
        for row in rows:
            account, login, password = row
            acc = Account(text=f'{account}',
                          size_hint_y=None,
                          size_hint_x=0.2)
            self.grid.add_widget(acc)

            log = Login(text=f'{login}',
                        size_hint_y=None,
                        size_hint_x=0.4)
            self.grid.add_widget(log)

            psw = Password(text=f'{password}',
                           size_hint_y=None,
                           size_hint_x=0.3)
            self.grid.add_widget(psw)

            check = Check(size_hint_y=None,
                          size_hint_x=0.1)
            check.bind(active=self.showPassword)
            self.grid.add_widget(check)

            self.rows.append([acc, log, psw, check])

    def showPassword(self, checkbox, value):
        for row in self.rows:
            if checkbox == row[3]:
                if value:
                    row[2].password = False
                else:
                    row[2].password = True

    def editCred(self):
        form = self.createForm()
        btn = Button(text='Confirmar',
                     size_hint=(1, 0.25),
                     font_size=20,
                     on_press=self.editAccount)
        form.add_widget(btn)
        popup = Popup(title='Edite os dados nos campos abaixo',
                      size_hint=(None, None),
                      size=(400, 300),
                      content=form)
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def editAccount(self, btn):
        self.user.editData(self.acc.text, self.login.text, self.psw.text)
        self.updateGrid()


    def addCred(self):
        form = self.createForm()
        btn = Button(text='Cadastrar',
                     size_hint=(1, 0.25),
                     font_size=20,
                     on_press=self.addAccount)
        form.add_widget(btn)
        popup = Popup(title='Cadastre uma conta',
                      size_hint=(None, None),
                      size=(400, 300),
                      content=form)
        btn.bind(on_release=popup.dismiss)
        popup.open()

    def removeCred(self, *args):
        box = BoxLayout(orientation='vertical')
        self.acc = Account(readonly=False, size_hint=(1, 0.6))
        box.add_widget(self.acc)

        btn = Button(text='Confirmar',
                     size_hint=(1, 0.4),
                     font_size=20)
        box.add_widget(btn)

        popup = Popup(title='Digite a conta a ser deletada',
                      size_hint=(None, None),
                      size=(400, 150),
                      content=box)

        btn.bind(on_release=self.removeWidget, on_press=popup.dismiss)
        popup.open()

    def removeWidget(self, btn):
        btn.disabled = True
        self.user.deleteData(self.acc.text)
        self.updateGrid()

    def addAccount(self, btn):
        btn.disabled = True
        if ((acc:=self.acc.text) != '') and ((log:=self.login.text) != '') and ((psw:=self.psw.text) != ''):
            self.user.writeData(acc, log, psw)
            acc = Account(text=acc,
                          size_hint_y=None,
                          size_hint_x=0.2)
            self.grid.add_widget(acc)

            log = Login(text=log,
                        size_hint_y=None,
                        size_hint_x=0.4)
            self.grid.add_widget(log)

            psw = Password(text=psw,
                           size_hint_y=None,
                           size_hint_x=0.3)
            self.grid.add_widget(psw)

            check = Check(size_hint_y=None,
                          size_hint_x=0.1)
            check.bind(active=self.showPassword)
            self.grid.add_widget(check)

            self.rows.append([acc, log, psw, check])

    def returnHome(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login'
        self.clear_widgets()
        App.get_running_app().loginScreen.clockTime.cancel()
        App.get_running_app().loginScreen.clockStop.cancel()
        self.user.authenticated = False
        self.user.disconnect()
        del self.user




