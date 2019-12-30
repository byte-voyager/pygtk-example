import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app, title):
        super(AppWindow, self).__init__(application=app, title=title)
        self.set_border_width(10)
        radio1 = Gtk.RadioButton.new_with_label(None, "I want to be clicked!")
        radio2 = Gtk.RadioButton.new_with_label_from_widget(radio1, "Click me instead!")
        radio3 = Gtk.RadioButton.new_with_label_from_widget(radio2, "No! Click me!")
        radio4 = Gtk.RadioButton.new_with_label_from_widget(radio3, "No! Click me instead!")
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.pack_start(radio1, False, False, 0)
        vbox.pack_start(radio2, False, False, 0)
        vbox.pack_start(radio3, False, False, 0)
        vbox.pack_start(radio4, False, False, 0)
        self.add(vbox)
        self.show_all()

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
