import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app, title):
        super(AppWindow, self).__init__(application=app, title=title)
        self.set_border_width(10)
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        check1 = Gtk.CheckButton.new_with_label("I am the main option.")
        check2 = Gtk.CheckButton.new_with_label("I am the second option.")
        check2.set_sensitive(False)
        check1.connect('toggled', self.on_button_checked, check2)
        close_button = Gtk.Button.new_with_mnemonic('_Close')
        close_button.connect('clicked', self.on_close_button_clicked)

        vbox.pack_start(check1, False, False, 0)
        vbox.pack_start(check2, False, True, 0)
        vbox2 = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)  # 垂直的盒子把水平占满
        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)  # 水平的盒子把垂直占满
        vbox.pack_start(hbox, True, True, 0)
        vbox2.pack_start(close_button, False, False, 0)

        vbox.pack_start(vbox2, False, True, 0)

        self.set_size_request(300, 300)
        self.add(vbox)

    @staticmethod
    def on_button_checked(check1, check2):
        if check1.get_active():
            check2.set_sensitive(True)
        else:
            check2.set_sensitive(False)

    def on_close_button_clicked(self, button):
        self.destroy()


class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="aa.cc")
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(app=self, title='Toggle Buttons')
        self.window.show_all()
        self.window.present()


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)
