import gi
import signal

signal.signal(signal.SIGINT, signal.SIG_DFL)

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, Gdk, Gio


class Flash(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, type=Gtk.WindowType.POPUP)

        self.set_app_paintable(True)  # Let the app paint itself, don't use system theme

        provider = Gtk.CssProvider()

        provider.load_from_file(Gio.File.new_for_path('./trans-style.css'))

        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider,
                                                 Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.get_style_context().add_class('red')


win = Flash()

win.show_all()

Gtk.main()
