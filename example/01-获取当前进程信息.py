import gi
import os
import sys
import subprocess

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def daemonize():
    pid = os.fork()
    if pid < 0:
        return False  # 创建失败
    if pid > 0:
        Gtk.main_quit()
        sys.exit(0)  # 父进程

    os.chdir('/')
    os.umask(0)

    # 创建新的会话 设置当前进程为进程组的首领
    try:
        os.setsid()
    except Exception as e:
        print(e)

    # os.close(sys.stdout)
    # os.close(sys.stdin)
    # os.close(sys.stderr)



class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        label = Gtk.Label.new('进程组ID:%s' % os.getpgid(os.getpid()))
        label2 = Gtk.Label.new('进程ID:%s' % os.getpid())
        label3 = Gtk.Label.new("Linux 每一个进程都隶属于进程组,每一个进程需都有一个首领进程,"
                               "其进程组id和pid相等。一些有关联的进程组会形成一个会话。")
        output = subprocess.getoutput("ps -o pid,ppid,pgid,sid,comm | less")
        label4 = Gtk.Label.new(output)
        button = Gtk.Button.new_with_label('创建一个守护进程')
        button.connect('clicked', self.on_button_clicked)
        print(output)
        vbox.pack_start(label, False, False, 0)
        vbox.pack_start(label2, False, False, 0)
        vbox.pack_start(label3, False, False, 0)
        vbox.pack_start(label4, False, False, 0)
        vbox.pack_start(button, False, False, 0)
        self.set_size_request(300, 300)
        self.add(vbox)

    def on_button_clicked(self, button):
        print('clicked')
        daemonize()


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
