import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

class MyWindow(Gtk.Window):

    key = Gdk.KEY_h

    def __init__(self):
        # init the base class (Gtk.Window)
        super().__init__()

        # state affected by shortcuts
        self.shortcut_hits = 0

        # Tell Gtk what to do when the window is closed (in this case quit the main loop)
        self.connect("delete-event", Gtk.main_quit)

        # connect the key-press event - this will call the keypress
        # handler when any key is pressed
        self.connect("key-press-event",self.on_key_press_event)

        # Window content goes in a vertical box
        box = Gtk.VBox()

        # mapping between Gdk.KEY_h and a string
        keyname = Gdk.keyval_name(self.key)

        # a helpful label
        instruct = Gtk.Label(label="Press Ctrl+%s" % keyname)
        box.add(instruct)

        # the label that will respond to the event
        self.label = Gtk.Label(label="")
        self.update_label_text()

        # Add the label to the window
        box.add(self.label)

        self.add(box)

    def on_key_press_event(self, widget, event):

        print("Key press on widget: ", widget)
        print("          Modifiers: ", event.state)
        print("      Key val, name: ", event.keyval, Gdk.keyval_name(event.keyval))

        # check the event modifiers (can also use SHIFTMASK, etc)
        ctrl = (event.state & Gdk.ModifierType.CONTROL_MASK)

        # see if we recognise a keypress
        if ctrl and event.keyval == Gdk.KEY_h:
            self.shortcut_hits += 1
            self.update_label_text()

    def update_label_text(self):
        # Update the label based on the state of the hit variable
        self.label.set_text("Shortcut pressed %d times" % self.shortcut_hits)

if __name__ == "__main__":
    win = MyWindow()
    win.show_all()

    # Start the Gtk main loop
    Gtk.main()