import threading
import time

from gi.repository import Gtk, GObject, Gdk, GLib


def app_main_deprecated():
    win = Gtk.Window(default_height=50, default_width=300)
    win.connect("delete-event", Gtk.main_quit)

    progress = Gtk.ProgressBar(show_text=True)

    def example_target():
        for i in range(50):
            Gdk.threads_enter()
            progress.pulse()
            progress.set_text(str(i))
            Gdk.threads_leave()
            time.sleep(0.2)

    def change_title_gdk(*args):
        win.set_title("change_title_gdk")
        return False

    Gdk.threads_add_timeout_seconds(
        GLib.PRIORITY_DEFAULT, 2, change_title_gdk, None)

    def change_title_glib(*args):
        Gdk.threads_enter()
        win.set_title("change_title_glib")
        Gdk.threads_leave()
        return False

    GLib.timeout_add_seconds(4, change_title_glib)

    def change_title_click(button):
        button.set_label("You clicked me")

    button = Gtk.Button(label="Click Me")
    button.connect("clicked", change_title_click)

    box = Gtk.Box()
    box.pack_start(button, False, True, 0)
    box.pack_start(progress, True, True, 0)
    win.add(box)
    win.show_all()

    thread = threading.Thread(target=example_target)
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    # Calling GObject.threads_init() is not needed for PyGObject 3.10.2+
    GObject.threads_init()

    Gdk.threads_init()
    Gdk.threads_enter()
    app_main_deprecated()
    Gtk.main()
    Gdk.threads_leave()