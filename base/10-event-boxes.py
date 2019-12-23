import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        eventbox = Gtk.EventBox.new()
        label = Gtk.Label.new('Double-Click Me!')
        eventbox.set_above_child(False)
        eventbox.connect('button_press_event', self.on_button_press, label)
        eventbox.add(label)
        self.add(eventbox)
        # eventbox.set_events(Gdk.EventMask.EXPOSURE_MASK)
        eventbox.realize()

    def on_button_press(self, eventbox, event, label):
        if event.type == Gdk.EventType._2BUTTON_PRESS:
            text = label.get_text()
            if text[0] == 'D':
                label.set_text("I Was Double-Clicked!")
            else:
                label.set_text("Double-Click Me Again")
        return False


class App(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id='aa.cc', **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title='Hello World!')
        self.window.show_all()
        self.window.present()


if __name__ == '__main__':
    import sys

    app = App()
    app.run(sys.argv)
