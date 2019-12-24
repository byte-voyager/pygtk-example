import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__(application_id='aa.xx')
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(title='button', app=self)
        self.window.show_all()
        self.window.present()


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, title, app):
        super().__init__(title=title, application=app)
        self.set_border_width(10)
        button = Gtk.Button.new()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        icon_theme = Gtk.IconTheme.get_default()
        icon = icon_theme.load_icon('window-close', -1, Gtk.IconLookupFlags.FORCE_SIZE)
        image = Gtk.Image.new_from_pixbuf(icon)
        hbox.add(image)
        label = Gtk.Label.new_with_mnemonic('_Close')
        # hbox.add(label)
        hbox.set_homogeneous(True)
        button.add(hbox)
        button.connect('clicked', self.on_button_clicked)
        button.set_relief(Gtk.ReliefStyle.NORMAL)
        self.add(button)
        self.set_size_request(230, 100)
        self.resize(300, 100)  #
        print(self.get_size())

    def on_button_clicked(self, param):
        self.destroy()


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)
