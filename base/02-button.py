import sys
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gdk


class AppWindow(Gtk.Window):
    def __init__(self, app, title):
        super().__init__(application=app, title=title)
        self.set_size_request(200, 100)
        button = Gtk.Button.new_with_mnemonic('H_ello _Close')  # 按住Alt+c 就会触发
        button.connect('clicked', self.on_button_clicked)

        button.set_relief(Gtk.ReliefStyle.NORMAL)
        button.set_size_request(600, 400)  # 这个才是最终的结果
        # allocation = Gdk.Rectangle(x=0 ,y=0, height=100, width=100)
        # print('al', allocation.height)
        # cairo = Gdk.cairo_create(self)

        # button.size_allocate(allocation=allocation)
        # button.size_allocate()
        print(button.get_allocated_width())  # 这里还获取不到的

        print(self.get_children())
        self.connect('add', self.on_add_trigger)
        self.connect('set-focus-child', self.on_focus_trigger)
        self.add(button)

    def on_button_clicked(self, button):
        self.destroy()

    def on_add_trigger(self, *args):
        print("add 信号")

    def on_focus_trigger(self, *args):
        print("set_focus_child")

class Application(Gtk.Application):
    def __init__(self):
        super(Application, self).__init__(application_id="org.example.myapp")
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(self, 'Hello World')
        self.window.show_all()
        print(self.window.get_allocated_width())
        self.window.present()


if __name__ == '__main__':
    app = Application()
    app.run(sys.argv)
