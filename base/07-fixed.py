#!/usr/bin/python3

import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.set_border_width(10)
        fixed = Gtk.Fixed.new()
        button1 = Gtk.Button.new_with_label("Pixel by pixel ...")
        button2 = Gtk.Button.new_with_label("you choose my fate.")
        button1.connect("clicked", self.on_button_clicked)
        button1.set_size_request(100, 50)
        button2.connect("clicked", self.on_button_clicked)
        fixed.put(button1, 0, 0)
        fixed.put(button2, 100, 50)
        self.add(fixed)
        self.connect('draw', self.on_draw)

        self.show_all()

    def on_button_clicked(self, widget):
        self.destroy()

    def on_draw(self, *args):
        import datetime
        print('draw', str(datetime.datetime.now()))


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Fixed")
        self.window.show_all()
        self.window.present()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
