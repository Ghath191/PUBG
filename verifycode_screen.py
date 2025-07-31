from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
import random
import smtplib
from email.mime.text import MIMEText

store = JsonStore("user_data.json")

# بيانات حساب Gmail للإرسال
FROM_EMAIL = "m.man1919191@gmail.com"
FROM_PASSWORD = "sual bghs oail ocpv"  # كلمة مرور التطبيقات

def send_email(to_email, code):
    subject = "Your Verification Code"
    body = f"Your verification code is: {code}"
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(FROM_EMAIL, FROM_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")

class VerifyCodeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = get_color_from_hex("#121212")  # خلفية داكنة
        self.code = None
        self.build_ui()

    def build_ui(self):
        self.layout = BoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20,
            size_hint=(0.85, 0.7),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        # العنوان الرئيسي
        title = Label(
            text="Verify Code",
            font_size=38,
            bold=True,
            color=get_color_from_hex("#FFFFFF"),  # أبيض للنص
            size_hint_y=None,
            height=60,
            halign="center",
        )

        # شرح أدنى العنوان
        self.info_label = Label(
            text="Enter the 6-digit verification code sent to your email.",
            font_size=18,
            color=get_color_from_hex("#AAAAAA"),  # رمادي فاتح للنص
            size_hint_y=None,
            height=40,
            halign="center",
        )

        # وصف عن PUBG
        self.pubg_desc = Label(
            text="PUBG is a popular battle royale game where players fight to be the last survivor.",
            font_size=16,
            italic=True,
            color=get_color_from_hex("#CCCCCC"),  # رمادي فاتح للنص
            size_hint_y=None,
            height=60,
            halign="center",
        )

        # حقل الإدخال للكود
        self.code_input = TextInput(
            hint_text="Enter 6-digit code",
            multiline=False,
            size_hint_y=None,
            height=50,
            padding_y=(10, 10),
            background_normal="",
            background_color=get_color_from_hex("#222222"),  # خلفية داكنة لحقل الإدخال
            foreground_color=get_color_from_hex("#FFFFFF"),  # نص أبيض
            cursor_color=get_color_from_hex("#1DB954"),  # لون المؤشر أخضر
            font_size=24,
            input_filter='int',
        )
        self.code_input.bind(text=self.limit_code_length)

        # رسالة الحالة (نجاح أو خطأ)
        self.status_label = Label(
            text="",
            color=get_color_from_hex("#E53935"),  # أحمر افتراضي للأخطاء
            size_hint_y=None,
            height=30,
            halign="center",
        )

        # زر إرسال الكود
        send_code_btn = Button(
            text="Send Code",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#1DB954"),  # أخضر زاهي
            color=get_color_from_hex("#FFFFFF"),
            font_size=18,
            bold=True,
        )
        send_code_btn.bind(on_release=self.send_code)

        # زر التحقق
        verify_btn = Button(
            text="Verify",
            size_hint_y=None,
            height=50,
            background_color=get_color_from_hex("#FF5722"),  # برتقالي زاهي
            color=get_color_from_hex("#FFFFFF"),
            font_size=18,
            bold=True,
        )
        verify_btn.bind(on_release=self.verify_code)

        # إضافة العناصر إلى الواجهة
        self.layout.add_widget(title)
        self.layout.add_widget(self.info_label)
        self.layout.add_widget(self.code_input)
        self.layout.add_widget(self.pubg_desc)
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(send_code_btn)
        self.layout.add_widget(verify_btn)

        self.add_widget(self.layout)

    def limit_code_length(self, instance, value):
        if len(value) > 6:
            instance.text = value[:6]

    def send_code(self, instance):
        user_data = store.get("user") if store.exists("user") else {}
        email = user_data.get("email")
        if not email:
            self.status_label.color = get_color_from_hex("#E53935")
            self.status_label.text = "No email found, please login first."
            return

        self.code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        store.put("user", code=self.code)

        send_email(email, self.code)
        self.status_label.color = get_color_from_hex("#388E3C")  # أخضر للنجاح
        self.status_label.text = f"Verification code sent to {email}"

    def verify_code(self, instance):
        entered_code = self.code_input.text.strip()
        if not entered_code:
            self.status_label.color = get_color_from_hex("#E53935")
            self.status_label.text = "Please enter the verification code."
            return

        saved_code = store.get("user").get("code") if store.exists("user") else None
        if entered_code == saved_code:
            self.status_label.color = get_color_from_hex("#388E3C")
            self.status_label.text = "Code verified successfully!"
            # لا تمسح النص هنا
            self.manager.current = "main"
        else:
            self.status_label.color = get_color_from_hex("#E53935")
            self.status_label.text = "Invalid code, please try again."
