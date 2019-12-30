import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_border_width(10)
        button = Gtk.Button.new_with_mnemonic("_Open Dialog")
        button.connect('clicked', self.on_open_button_clicked, self)
        self.add(button)
        self.set_size_request(200, 200)

    @staticmethod
    def on_open_button_clicked(button, parent):
        dialog = Gtk.Dialog(title='Information', parent=parent, flags=Gtk.DialogFlags.MODAL)
        dialog.add_button('Ok', Gtk.ResponseType.OK)
        label = Gtk.Label('The Button was clicked!')
        image = Gtk.Image.new_from_icon_name('dialog-information', Gtk.IconSize.DIALOG)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        hbox.pack_start(image, False, False, 0)
        hbox.pack_start(label, False, False, 0)
        dialog.vbox.pack_start(hbox, False, False, 0)
        dialog.show_all()
        res = dialog.run()
        print('res', res)
        dialog.destroy()


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