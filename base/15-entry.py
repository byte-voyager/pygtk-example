import gi
import os
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        prompt_str = "hello, please input your password!"
        question = Gtk.Label(prompt_str)
        label = Gtk.Label('Password:')

        passwd = Gtk.Entry()
        passwd.set_visibility(False)
        passwd.set_invisible_char("*")

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(question, True, False, 0)

        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.pack_start(label, False, False, 0)
        hbox.pack_start(passwd, True, True, 0)
        vbox.pack_start(hbox, True, True, 0)

        self.add(vbox)


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp", **kwargs)  # 如果再次运行会查找此程序 存在这个id就只是再展现
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Main Window")
        self.window.show_all()
        self.window.present()


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)