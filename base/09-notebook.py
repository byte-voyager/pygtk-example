import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, application, title):
        super().__init__(title=title, application=application)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.set_border_width(10)
        # self.set_size_request(250, 100)
        notebook = Gtk.Notebook.new()
        label1 = Gtk.Label.new('Page 1')
        label2 = Gtk.Label.new('Page 2')
        child1 = Gtk.Label.new('This is page 1')
        child2 = Gtk.Label.new('This is page 2')
        notebook.append_page(child1, label1)
        notebook.append_page(child2, label2)

        notebook.set_tab_pos(Gtk.PositionType.TOP)
        # notebook.set_show_border(True)
        # notebook.set_show_tabs(False)

        box.pack_start(notebook, True, True, 0)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_next = Gtk.Button.new_with_mnemonic('_Next')
        button_next.connect('clicked', self.on_next_bt_clicked, notebook)
        button_prev = Gtk.Button.new_with_mnemonic('_Prev')
        button_prev.connect('clicked', self.on_prev_bt_clicked, notebook)
        hbox.pack_start(button_prev, True, True, 0)
        hbox.pack_start(button_next, True, True, 0)

        box.pack_start(hbox, False, False, 0)

        self.add(box)

    def on_next_bt_clicked(self, widget, notebook):
        cur_page = notebook.get_current_page()
        notebook.set_current_page(cur_page + 1)

    def on_prev_bt_clicked(self, widget, notebook):
        cur_page = notebook.get_current_page()
        notebook.set_current_page(cur_page - 1)


class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__(application_id="aa.cc")
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(title="Notebook", application=self)
        self.window.show_all()
        self.window.present()


if __name__ == '__main__':
    import sys

    app = Application()
    app.run(sys.argv)
