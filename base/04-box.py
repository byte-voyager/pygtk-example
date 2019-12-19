import sys
import gi
import random

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
from gi.repository import Gdk, Gtk

names = ["_Andrew", "_Joe", "_Samantha", "_Jonathan"]


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super(AppWindow, self).__init__(*args, **kwargs)
        # homogeneous 参数设置了之后 spacing参数就没用了
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, homogeneous=False, spacing=10)
        print(vbox.get_homogeneous())
        for name in names:
            button = Gtk.Button.new_with_mnemonic(name)
            rand_spacing = random.randint(1, 100)
            print('rand_spacing', rand_spacing)
            vbox.pack_start(button, True, False, rand_spacing)  # 第二个参数True窗口变大会将button变大
            button.connect('clicked', self.on_button_clicked)
            button.set_relief(Gtk.ReliefStyle.NORMAL)
            button.set_size_request(-1, 60)

        self.set_border_width(10)
        self.set_size_request(200, -1)  # 高度-1代表用它自己计算的高度
        self.add(vbox)

    def on_button_clicked(self, widget):
        self.destroy()


class App(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = None

    def do_activate(self):
        if self.window is None:
            self.window = AppWindow(title="Boxes", application=self)

        self.window.show_all()
        self.window.present()


if __name__ == '__main__':
    app = App()
    app.run(sys.argv)
