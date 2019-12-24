import gi
import sys
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, type=Gtk.WindowType.POPUP,**kwargs)
        label2 = Gtk.Label.new_with_mnemonic("_Hello World!")
        self.set_border_width(10)
        self.move(0, 0)

        self.set_name('GtkWindow')
        screen = Gdk.Screen.get_default()
        visual = Gdk.Screen.get_rgba_visual(screen)
        # visual = screen.get_system_visual()
        print(screen.get_root_window().get_height())
        self.set_decorated(False)
        self.set_visual(visual)
        self.fullscreen()
        style_context = label2.get_style_context()  # 得到label的style context
        css_provider = Gtk.CssProvider.new()  # 创建一个css provide
        # self.set_app_paintable(True)
        self.set_keep_above(True)
        root_window = Gdk.get_default_root_window()
        # self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)

        r = screen.get_monitor_workarea(0)

        print(r.width, r.height)

        h = r.height / 2 - 150
        w = r.width / 2 - 200
        self.move(w, h)
        label2.set_name('label1')
        css_provider.load_from_path('my_style2.css')  # 加载css文件

        # label.set_name('hello_label')

        print("screen.get_height: ", screen.get_height())
        Gtk.StyleContext.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
        # style_context.add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

        self.add(label2)
        # self.set_size_request(200, 100)
        print("children", self.get_children())
        child1: Gtk.Label = self.get_children()[0]
        print("child1.get_text(): ", child1.get_text())


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