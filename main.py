import os
import random
import threading
import urllib.request
import requests
from kivy.clock import Clock
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.snackbar import Snackbar
from plyer import filechooser
from android.permissions import request_permissions, Permission
request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
from android.storage import primary_external_storage_path
primary_ext_storage = primary_external_storage_path()


class First(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_name)

    def set_toolbar_font_name(self, *args):
        self.ids.toolbar.ids.label_title.font_name = "Lato-Regular.ttf"

    def do(self):
        scr = self.manager.get_screen('scr2')
        pat = scr.ids['image']
        try:
            pat.ii = str(pt)
        except NameError:
            pass
        spin = scr.ids['spinner']
        if not spin.active:
            spin.active = True
        else:
            spin.active = False


class Second(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_once(self.set_toolbar_font_name)

    def set_toolbar_font_name(self, *args):
        self.ids.toolbar.ids.label_title.font_name = "Lato-Regular.ttf"

    def re(self):
        scr = self.manager.get_screen('scr2')
        spin = scr.ids['spinner']
        spin.active = False


class SM(ScreenManager):
    def __init__(self, **kwargs):
        super(SM, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_key)

    def on_key(self, window, key, *args):
        if key == 27:
            if self.current_screen.name == "scr1":
                return False
            elif self.current_screen.name == "scr2":
                self.current = "scr1"
                return True


class RemoveApp(MDApp):
    selection = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        def connect(host='http://google.com'):
            try:
                urllib.request.urlopen(host)  # Python 3.x
                return True
            except:
                return False

        if connect():
            pass
        else:
            Snackbar(
                text="No Connection",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

        self.ext = ''

    def build(self):
        self.theme_cls.primary_palette = "Green"
        kv = Builder.load_file("main.kv")
        return SM()

    def file_manager_open(self):
        fil = [("Images", "*.jpg", "*.jpeg", "*.png")]
        filechooser.open_file(on_selection=self.handle_selection, filters=fil, multiple=True)

        perd = os.path.join(primary_ext_storage, 'Bg Removo')
        try:
            os.mkdir(perd)
        except FileExistsError:
            pass

    def handle_selection(self, selection):
        self.selection = selection
        return self.selection

    def on_selection(self, *a, **k):
        threading.Thread(target=self.t_thread).start()

    def end(self):
        try:
            if self.response.status_code == 402 or self.response.status_code == 403:
                fs.remove(fg)
                fg.replace(rkey, fg)
                Snackbar(
                    text="Something Gone Wrong, Go Back And Try Again",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(
                                        Window.width - (dp(10) * 2)
                                ) / Window.width
                ).open()
            elif self.response.status_code == 200:
                Snackbar(
                    text="Upload Complete",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(
                                        Window.width - (dp(10) * 2)
                                ) / Window.width
                ).open()
            else:
                Snackbar(
                    text="No Image Is Uploaded",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(
                                        Window.width - (dp(10) * 2)
                                ) / Window.width
                ).open()

        except AttributeError:
            pass

    def t_thread(self):
        global pt
        pt = self.selection[0]
        global fs
        fs = ['Api keys will be here']
        global fg
        global rkey
        rkey = random.choice(fs)
        fg = rkey
        try:
            self.response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(pt, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': fg},
            )

        except requests.exceptions.ConnectionError:
            self.no_connection()

        except IOError:
            self.fil_error()

    def no_connection(self):
        toast('No Connection')

    def fil_error(self):
        toast("No File is Selected")

    def remove(self, save_as):
        if save_as is "":
            save_as = 'no_bg'
        if self.ext is "":
            self.ext = 'png'
        try:
            if self.response.status_code == requests.codes.ok:
                with open(primary_ext_storage + '/Bg Removo/' + save_as + '.' + self.ext, 'wb') as out:
                    out.write(self.response.content)
                Snackbar(
                    text="Successfully Saved Check It In Your Gallery Or Filemanager",
                    snackbar_x="10dp",
                    snackbar_y="10dp",
                    size_hint_x=(
                                        Window.width - (dp(10) * 2)
                                ) / Window.width
                ).open()
            else:
                print("Error:", self.response.status_code)
        except AttributeError:
            Snackbar(
                text="Select Image Again",
                snackbar_x="10dp",
                snackbar_y="10dp",
                size_hint_x=(
                                    Window.width - (dp(10) * 2)
                            ) / Window.width
            ).open()

    def show_theme_picker(self):
        theme_dialog = MDThemePicker()
        theme_dialog.open()

    @mainthread
    def uploading(self):
        pass


if __name__ == '__main__':
    RemoveApp().run()
