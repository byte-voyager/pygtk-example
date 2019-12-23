import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

"""Gtk.Expander 容器只能包含一个child 通过点击expander的三角型按钮就可以隐藏显示"""


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        self.set_size_request(200, 100)
        expander = Gtk.Expander.new_with_mnemonic('Click _Me For More!')
        label = Gtk.Label.new("Hide me or show me.\nthat is your choice.")
        expander.add(label)
        expander.set_expanded(False)
        self.add(expander)


class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__(application_id="aa.cc")
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self, title="Hello")
            self.window.show_all()
            self.window.present()


if __name__ == "__main__":
    import sys

    app = Application()
    app.run(sys.argv)
