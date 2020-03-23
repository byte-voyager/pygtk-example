import gi
import os
import signal

gi.require_version('Gtk', '3.0')
gi.require_version('Keybinder', '3.0')

from gi.repository import Gtk
from gi.repository import Keybinder

signal.signal(signal.SIGCHLD, signal.SIG_IGN)


def run_other_window():
    pid = os.fork()
    if pid == 0:
        os.execlp('python', 'python', '../base/01-helloworld.py')
    print('run_other_window, pid', pid)


def callback(keystr, user_data):
    print("Handling", keystr, user_data)
    print("Event time:", Keybinder.get_current_event_time())
    run_other_window()


if __name__ == '__main__':
    keystr = "<Control><Alt>u"
    Keybinder.init()
    res = Keybinder.bind(keystr, callback, "Keystring %s (user data)" % keystr)
    if not res:
        print('绑定快捷键失败')
        exit(1)
    print("Press", keystr, "to handle keybinding and quit")
    Gtk.main()
