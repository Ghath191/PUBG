from kivy.app import App  
from kivy.uix.screenmanager import ScreenManager  
from login_screen import LoginScreen  
from verifycode_screen import VerifyCodeScreen  
from main_screen import MainScreen  
from pubg_screen import PubgScreen  

APP_VERSION = "1.0.0"

class MyApp(App):  
    def build(self):  
        sm = ScreenManager()  
        sm.add_widget(LoginScreen(name="login"))  
        sm.add_widget(VerifyCodeScreen(name="verify"))  
        sm.add_widget(MainScreen(name="main"))  
        sm.add_widget(PubgScreen(name="pubg"))  

        sm.current = "login"  
        return sm  
  
if __name__ == "__main__":  
    app = MyApp()
    app.icon = "assets/icon.png"  # تأكد من وجود هذا الملف
    app.run()
