from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout

class PubgScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        self.background = Image(source='pubg_bg.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        self.anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        
        self.layout = BoxLayout(
            orientation='vertical', 
            padding=40, 
            spacing=30, 
            size_hint=(0.8, 0.6)
        )

        self.status_label = Label(
            text="Press Start to begin",
            font_size=24,
            size_hint_y=None,
            height=60,
            color=get_color_from_hex("#FFC107"),
            halign="center"
        )
        self.layout.add_widget(self.status_label)

        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=40
        )
        self.layout.add_widget(self.progress)

        self.start_btn = Button(
            text="Start",
            size_hint_y=None,
            height=60,
            background_color=get_color_from_hex("#FF5722"),
            color=get_color_from_hex("#FFFFFF"),
            font_size=22,
            bold=True
        )
        self.start_btn.bind(on_release=self.start_loading)
        self.layout.add_widget(self.start_btn)

        self.anchor_layout.add_widget(self.layout)
        self.add_widget(self.anchor_layout)

        self._event = None

    def start_loading(self, instance):
        self.progress.value = 0
        self.status_label.text = "Loading..."
        self.start_btn.disabled = True
        self._event = Clock.schedule_interval(self.update_progress, 0.15)

    def update_progress(self, dt):
        if int(self.progress.value) % 20 == 0 and self.progress.value != 0:
            if hasattr(self, '_pause'):
                if self._pause:
                    self._pause = False
                    self.progress.value += 2
                else:
                    self._pause = True
            else:
                self._pause = True
        else:
            if not hasattr(self, '_pause') or not self._pause:
                self.progress.value += 2
        
        if self.progress.value >= 100:
            Clock.unschedule(self._event)
            self.status_label.text = "Request submitted!"
            self.start_btn.disabled = False
            self.manager.current = "verify"  # تم التعديل هنا ليروح على شاشة التحقق مباشرة
