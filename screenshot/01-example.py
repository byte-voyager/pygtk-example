import gi

gi.require_version("Gtk", '3.0')
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import GdkPixbuf, GLib

root_window = Gdk.get_default_root_window()
children = root_window.get_children()
print('children len', len(children))
print(children[0].get_geometry())

display: Gdk.Display = Gdk.Display.get_default()
screen = display.get_default_screen()
print('screen.get_height()', screen.get_height())
monitor1 = display.get_monitor(1)
print(monitor1.get_geometry().width, monitor1.get_geometry().height )
monitor0 = display.get_monitor(0)
# Gdk.beep()
print(monitor0.get_geometry().width, monitor0.get_geometry().height )
#
# pixbuf: GdkPixbuf.Pixbuf = Gdk.pixbuf_get_from_window(root_window, 0, 0, 1920+1366,
#                                                       1080)  # 截图两个屏幕

pixbuf: GdkPixbuf.Pixbuf = Gdk.pixbuf_get_from_window(root_window, 0, 0, 1920,
                                                      1080)  # 截图第一个个屏幕

print('devices')
# devices_manager = display.get_device_manager()
seat: Gdk.Seat = display.get_default_seat()
print(seat.get_keyboard().get_n_keys())
ll = seat.get_slaves(Gdk.SeatCapabilities.KEYBOARD)
for i in ll:
    print(i.get_name())

# print(type(pixbuf))
Gdk.flush()
pixbuf.savev("hello2.png", "png", '', '')

# window = Gtk.Window()
# window.show_all()

# print(Gdk.Screen.height(), Gdk.Screen.width())
# print(dir(Gdk.Screen.get_default().get_active_window()))
# print(Gdk.Screen.get_default().get_active_window())


# print(Gdk.Screen.get_default().get_active_window().get_desktop())
# print(Gdk.Screen.get_default().get_active_window().hide())


# def a(_):
#     print("sdsd")
#     # Gdk.Screen.get_default().get_active_window().destroy()
#     # Gtk.main_quit()
#     print("隐藏")
#     import time
#     while 1:
#         time.sleep(1)
#         print('sleep')


# GLib.timeout_add(2000, a, None)
# Gtk.main()
