#!/usr/bin/python3

import sys
import cairo
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

SIZE = 30


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_size_request(450, 550)
        screen = Gdk.Screen.get_default()
        visual = Gdk.Screen.get_rgba_visual(screen)
        print(Gdk.Screen.is_composited(screen))
        self.set_visual(visual)
        self.set_app_paintable(True)

        eventbox = Gtk.EventBox.new()
        eventbox.set_above_child(False)

        drawingarea = Gtk.DrawingArea()
        eventbox.connect('motion-notify-event', self.on_motion)
        eventbox.connect('button-press-event', self.on_press)
        eventbox.set_events(Gdk.EventMask.POINTER_MOTION_MASK)
        eventbox.add(drawingarea)

        self.add(eventbox)
        drawingarea.connect('draw', self.draw)

    def on_press(self, *args):
        import datetime
        print(str(args[1].type))

        print('args', *args, len(args))
        print('press', str(datetime.datetime.now()))

    def on_motion(self, *args):
        import datetime
        print(args)
        print(str(args[1].type))

        # print(Gdk.EventMotion.state)
        print(str(args[1].state))
        if args[1].state == Gdk.ModifierType.BUTTON1_MASK:
            print("你按下鼠标左键, dir(args[1])", dir(args[1]))
            self.move(args[1].x_root, args[1].y_root)
            print('x', args[1].x)

        print('args', *args, len(args))
        print('motion', str(datetime.datetime.now()))

    def triangle(self, ctx):
        ctx.move_to(SIZE, 0)
        ctx.rel_line_to(SIZE, 2 * SIZE)
        ctx.rel_line_to(-2 * SIZE, 0)
        ctx.close_path()

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

    def inf(self, ctx):
        ctx.move_to(0, SIZE)
        ctx.rel_curve_to(0, SIZE, SIZE, SIZE, 2 * SIZE, 0)
        ctx.rel_curve_to(SIZE, -SIZE, 2 * SIZE, -SIZE, 2 * SIZE, 0)
        ctx.rel_curve_to(0, SIZE, -SIZE, SIZE, -2 * SIZE, 0)
        ctx.rel_curve_to(-SIZE, -SIZE, -2 * SIZE, -SIZE, -2 * SIZE, 0)
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
        ctx.new_path()
        ctx.translate(3 * SIZE, 0)
        self.square(ctx)
        if fill:
            ctx.fill()
        else:
            ctx.stroke()
        ctx.new_path()
        ctx.translate(3 * SIZE, 0)
        self.triangle(ctx)
        if fill:
            ctx.fill()
        else:
            ctx.stroke()
        ctx.new_path()
        ctx.translate(3 * SIZE, 0)
        self.inf(ctx)
        if fill:
            ctx.fill()
        else:
            ctx.stroke()
        ctx.restore()

    def fill_shapes(self, ctx, x, y):
        self.draw_shapes(ctx, x, y, True)

    def stroke_shapes(self, ctx, x, y):
        self.draw_shapes(ctx, x, y, False)

    def draw(self, da, ctx):
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(SIZE / 4)
        ctx.set_tolerance(0.1)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        ctx.set_dash([SIZE / 4.0, SIZE / 4.0], 0)
        self.stroke_shapes(ctx, 0, 0)
        ctx.set_dash([], 0)
        self.stroke_shapes(ctx, 0, 3 * SIZE)
        ctx.set_line_join(cairo.LINE_JOIN_BEVEL)
        self.stroke_shapes(ctx, 0, 6 * SIZE)
        ctx.set_line_join(cairo.LINE_JOIN_MITER)
        self.stroke_shapes(ctx, 0, 9 * SIZE)
        self.fill_shapes(ctx, 0, 12 * SIZE)
        ctx.set_line_join(cairo.LINE_JOIN_BEVEL)
        self.fill_shapes(ctx, 0, 15 * SIZE)
        ctx.set_source_rgb(1, 0, 0)
        self.stroke_shapes(ctx, 0, 15 * SIZE)


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         **kwargs)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = AppWindow(application=self,
                                    title="Drawing Areas", type=Gtk.WindowType.POPUP)
        self.window.show_all()
        self.window.present()


if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
