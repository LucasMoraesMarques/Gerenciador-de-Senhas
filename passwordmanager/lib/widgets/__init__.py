from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class Account(TextInput):
    pass


class Login(TextInput):
    pass


class Password(TextInput):
    pass


class Check(CheckBox):
    pass


class EnterPopup(Popup):
    pass


class RegisterPopupError(Popup):
    def __init__(self, **kwargs):
        super(RegisterPopupError, self).__init__(**kwargs)



