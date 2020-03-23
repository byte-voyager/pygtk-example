#!/usr/bin/python3

import sys
import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
import time
SIZE = 30

root_window = Gdk.get_default_root_window()
children = root_window.get_children()
print('children len', len(children))
print(children[0].get_geometry())

display: Gdk.Display = Gdk.Display.get_default()
monitor1 = display.get_monitor(1)
print(monitor1.get_geometry().width, monitor1.get_geometry().height )
monitor0 = display.get_monitor(0)
# Gdk.beep()
print(monitor0.get_geometry().width, monitor0.get_geometry().height )
#
# pixbuf: GdkPixbuf.Pixbuf = Gdk.pixbuf_get_from_window(root_window, 0, 0, 1920+1366,
#                                                       1080)  # 截图两个屏幕 768

pixbuf: GdkPixbuf.Pixbuf = Gdk.pixbuf_get_from_window(root_window, 1920, 0, 1366,
                                                      768)  # 截图第2个个屏幕

# print(type(pixbuf))
Gdk.flush()

class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(450, 550)
        # eventbox = Gtk.EventBox.new()
        # eventbox.set_above_child(False)

        drawingarea = Gtk.DrawingArea()
        self.add(drawingarea)
        self.surface = None
        Gdk.Window.create_similar_surface()
        # self.add(eventbox)
        drawingarea.set_events(Gdk.EventMask.POINTER_MOTION_MASK|Gdk.EventMask.BUTTON_PRESS_MASK)
        drawingarea.connect('motion-notify-event', self.motion_notify_event_cb)
        drawingarea.connect('draw', self.draw)

    def motion_notify_event_cb(self, widget: Gtk.DrawingArea, event, data=None):

        # print('motion_notify_event_cb', time.time())
        if event.state == Gdk.ModifierType.BUTTON1_MASK:
            print("你按下鼠标左键")
            print(self.ctx)
            self.stroke_shapes(self.ctx, 0, 0)
            widget.queue_draw()
            # self.move(args[1].x_root, args[1].y_root)
            # print('x', args[1].x)

    def square(self, ctx):
        ctx.move_to(0, 0)
        ctx.rel_line_to(2 * SIZE, 0)
        ctx.rel_line_to(0, 2 * SIZE)
        ctx.rel_line_to(-2 * SIZE, 0)
        ctx.close_path()


    def bowtie(self, ctx):
        ctx.move_to(0, 0)
        ctx.rel_line_to(2 * SIZE, 2 * SIZE)
        ctx.rel_line_to(-2 * SIZE, 0)
        ctx.rel_line_to(2 * SIZE, -2 * SIZE)
        ctx.close_path()

    def draw_shapes(self, ctx, x, y, fill):
        ctx.save()
        ctx.new_path()
        ctx.translate(x + SIZE, y + SIZE)
        self.bowtie(ctx)
        if fill:
            ctx.fill()
        else:
            ctx.stroke()
        # ctx.new_path()
        # ctx.translate(3 * SIZE, 0)
        # self.square(ctx)
        # if fill:
        #     ctx.fill()
        # else:
        #     ctx.stroke()
        # ctx.new_path()
        # ctx.translate(3 * SIZE, 0)
        # self.triangle(ctx)
        # if fill:
        #     ctx.fill()
        # else:
        #     ctx.stroke()
        # ctx.new_path()
        # ctx.translate(3 * SIZE, 0)
        # self.inf(ctx)
        # if fill:
        #     ctx.fill()
        # else:
        #     ctx.stroke()
        # ctx.restore()

    def stroke_shapes(self, ctx, x, y):
        self.draw_shapes(ctx, x, y, False)

    def draw(self, da, ctx:cairo.Context):
        self.ctx = ctx
        print('ok')
        print(pixbuf)
        Gdk.cairo_set_source_pixbuf(ctx, pixbuf, 0, 0)
        ctx.paint()
        ctx.set_source_rgb(255, 0, 0)
        ctx.set_line_width(SIZE / 4)
        ctx.set_tolerance(0.1)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_dash([SIZE / 4.0, SIZE / 4.0], 0)
        self.stroke_shapes(ctx, 0, 0)
        # ctx.get_target().write_to_png('./a.png')
        # return True

class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self,
                                    title="Drawing Areas", type=Gtk.WindowType.TOPLEVEL)
        self.window.show_all()
        self.window.present()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
