#!/usr/bin/python3

import sys
import time
import cairo
import math
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf


def colorHexToCairo(color):
    """
    Convert a html (hex) RGB value to cairo color.

    @type color: html color string
    @param color: The color to convert.
    @return: A color in cairo format.
    """
    if color[0] == '#':
        color = color[1:]
    (r, g, b) = (int(color[:2], 16),
                 int(color[2:4], 16),
                 int(color[4:], 16))
    return colorRGBToCairo((r, g, b))


def colorRGBToCairo(color):
    """
    Convert a 8 bit RGB value to cairo color.

    @type color: a triple of integers between 0 and 255
    @param color: The color to convert.
    @return: A color in cairo format.
    """
    return (color[0] / 255.0, color[1] / 255.0, color[2] / 255.0)

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
        self.set_size_request(500, 500)
        # eventbox = Gtk.EventBox.new()
        # eventbox.set_above_child(False)

        self.drawingarea = Gtk.DrawingArea()
        self.add(self.drawingarea)
        self.surface = None
        # Gdk.Window.create_similar_surface()
        # self.add(eventbox)
        self.drawingarea.set_events(Gdk.EventMask.POINTER_MOTION_MASK|Gdk.EventMask.BUTTON_PRESS_MASK|Gdk.EventMask.BUTTON_RELEASE_MASK)
        self.drawingarea.connect('motion-notify-event', self.motion_notify_event_cb)
        self.drawingarea.connect('button-release-event', self.button_release)
        self.connect("key-press-event",self.on_key_press_event)
        self.drawingarea.connect('draw', self.draw)

        self.start_x = 0
        self.start_y = 0

        self.x = 255
        self.y = 255
        self.start = False
        self.cur_action = 0
        self.arrow_action = []

    def button_release(self, *args):
        print('button release')
        self.start = False
        self.arrow_action.append((self.start_x, self.start_y, self.x, self.y))
        self.drawingarea.queue_draw()
        self.cur_action = -1

    def motion_notify_event_cb(self, widget: Gtk.DrawingArea, event, data=None):

        # print('motion_notify_event_cb', time.time())
        if event.state == Gdk.ModifierType.BUTTON1_MASK:
            # print("你按下鼠标左键")
            if self.start is False:
                self.start = True
                self.start_x = event.x
                self.start_y = event.y
                return
            self.x = event.x
            self.y = event.y
            widget.queue_draw()
            self.cur_action = 0
            # self.move(args[1].x_root, args[1].y_root)
            # print('x', args[1].x)
            return False

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



    def on_key_press_event(self, widget, event):

        # print("Key press on widget: ", widget)
        # print("          Modifiers: ", event.state)
        # print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_z:
            print(self.arrow_action)
            if self.arrow_action:
                self.arrow_action.pop()
            self.start_x = self.start_y = self.x = self.y = 0
            self.drawingarea.queue_draw()

        if ctrl and event.keyval == Gdk.KEY_s:
            print(self.get_size())
            pixbuf: GdkPixbuf.Pixbuf  = Gdk.pixbuf_get_from_window(self.get_window(), 0, 0,  *self.get_size())
            pixbuf.savev(str(time.time())+".png", "png", '', '')

    def drawArrow(self, cr, sx, sy, ex, ey, color, size):
        '''Draw arrow.'''
        # Init.
        arrowSize = size * 4             # in pixe
        arrowAngle = 10             # in degree

        # Draw arrow body.
        lineWidth = math.fabs(sx - ex)
        lineHeight = math.fabs(sy - ey)
        lineSide = math.sqrt(pow(lineWidth, 2) + pow(lineHeight, 2))
        offsetSide = arrowSize * math.sin(arrowAngle)
        if lineSide == 0:
            offsetX = offsetY = 0
        else:
            offsetX = offsetSide / lineSide * lineWidth
            offsetY = offsetSide / lineSide * lineHeight

        if ex >= sx:
            offsetX = -offsetX
        if ey >= sy:
            offsetY = -offsetY

        cr.move_to(sx, sy)
        cr.line_to(ex - offsetX, ey - offsetY)
        cr.set_source_rgb(*colorHexToCairo(color))
        cr.set_line_width(size)
        cr.stroke()

        # Draw arrow head.

        angle = math.atan2(ey - sy, ex - sx) + math.pi # 根据反tan函数 传入对边和邻边 得到角度
        x2 = ex - arrowSize * math.cos(angle - arrowAngle)
        y2 = ey - arrowSize * math.sin(angle - arrowAngle)

        x1 = ex - arrowSize * math.cos(angle + arrowAngle)  # 对边比斜边 根据已知的角度和斜边长度 得到对边长度
        y1 = ey - arrowSize * math.sin(angle + arrowAngle)  # 邻边比斜边 根据已知的角度个斜边长度 得到邻边长度

        cr.move_to(ex, ey)
        cr.line_to(x1, y1)
        cr.line_to(x2, y2)
        cr.fill()

    def draw(self, widget, ctx:cairo.Context):
        # print('draw    self', self, widget)
        Gdk.cairo_set_source_pixbuf(ctx, pixbuf, 0, 0)
        # # ctx.paint()
        # ctx.set_source_rgb(255, 0, 0)
        # ctx.set_line_width(SIZE / 4)
        # ctx.set_tolerance(0.1)
        # ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        # ctx.set_dash([SIZE / 4.0, SIZE / 4.0], 0)
        # self.stroke_shapes(ctx, 0, 0)
        # ctx.move_to(0, 0)
        # ctx.line_to(10, 10)
        # ctx.get_target().write_to_png('./a.png')
        # return True
        ctx.paint()
        ctx.set_line_width(10)
        ctx.set_source_rgb(255, 0, 0)
        # ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        # ctx.move_to(self.start_x, self.start_y)
        # ctx.line_to(self.x, self.y)
        # ctx.stroke()

        # ctx.move_to(self.x, self.y)
        # ctx.line_to(self.x, self.y+20)
        # ctx.line_to(self.x+20, self.y)
        # ctx.stroke()

        # if self.cur_action == 0:
        self.drawArrow(ctx, self.start_x, self.start_y, self.x, self.y, '#FF0000', 7)
        for sx, sy, ex, ey in self.arrow_action:
            self.drawArrow(ctx, sx, sy, ex, ey, '#FF0000', 7)

        # ctx.scale(WIDTH, HEIGHT)  # Normalizing the canvas



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
