import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        color = Gdk.RGBA(red=0, green=.33, blue=.66, alpha=1.0)
        color = Gdk.RGBA.to_color(color)
        button = Gtk.ColorButton.new_with_color(color)
        button.set_title("Select a Color!")
        label = Gtk.Label("Look at my color!")
        label.modify_fg(Gtk.StateType.NORMAL, color)
        button.connect("color_set", self.on_color_changed, label)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.pack_start(button, False, False, 5)
        hbox.pack_start(label, False, False, 5)
        self.add(hbox)

    def on_color_changed(self, button, label):
        color = button.get_color()
        print(color)
        label.modify_fg(Gtk.StateType.NORMAL, color)


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
