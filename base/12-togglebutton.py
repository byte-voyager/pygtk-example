import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app, title):
        super(AppWindow, self).__init__(application=app, title=title)
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        toggle1 = Gtk.ToggleButton.new_with_mnemonic("_Deactivate the other one!")
        toggle2 = Gtk.ToggleButton.new_with_mnemonic("_No! Deactivate the other one!")
        toggle1.connect('toggled', self.on_button_toggle, toggle2)
        toggle2.connect('toggled', self.on_button_toggle, toggle1)
        vbox.pack_start(toggle1, True, True, 1)
        vbox.pack_start(toggle2, True, True, 1)

        self.add(vbox)

    @staticmethod
    def on_button_toggle(toggle, other_toggle: Gtk.ToggleButton):
        if Gtk.ToggleButton.get_active(toggle):
            other_toggle.set_sensitive(False)
        else:
            other_toggle.set_sensitive(True)


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
