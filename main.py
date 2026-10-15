
#!/usr/bin/env python3

# DO NOT CHANGE IMPORT ORDER, TURN OFF ANY FORMATTER
from ctypes import CDLL
CDLL('libgtk4-layer-shell.so')

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Gtk4LayerShell', '1.0')

from gi.repository import Gtk, Gdk
from gi.repository import Gtk4LayerShell as LayerShell  # pyright: ignore[reportAttributeAccessIssue]

def onActivate(app):
    # Window boiler plate
    window = Gtk.ApplicationWindow(application=app)
    window.set_title('Task Pins')
    window.set_default_size(750, 240)
    window.set_decorated(False)

    # Put the window on an overlay layer
    LayerShell.init_for_window(window)
    LayerShell.set_layer(window, LayerShell.Layer.OVERLAY)

    # Pin the shit to the top left
    LayerShell.set_anchor(window, LayerShell.Edge.TOP, True)
    LayerShell.set_anchor(window, LayerShell.Edge.LEFT, True)

    # Don't steal keyboard focus cause we're good boys
    LayerShell.set_keyboard_mode(
        window, LayerShell.KeyboardMode.NONE
    )

    # Add some CSS
    css = Gtk.CssProvider()
    css.load_from_data(b'''
        window {
            background-color: transparent;
        }

        .overlay-card {
            background-color: rgba(25, 25, 35, 0.85);
            padding: 14px;
        }
    ''')

    # Set the style
    display = Gdk.Display.get_default()
    if display is None:
        raise RuntimeError("No GDK display available")

    Gtk.StyleContext.add_provider_for_display(
        display,
        css,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
    )

    # Put the shit in the container
    card = Gtk.Box(
        orientation=Gtk.Orientation.VERTICAL,
        spacing=6,
    )
    card.add_css_class('overlay-card')

    window.set_child(card)
    window.present()


app = Gtk.Application(
    application_id='dev.finbear.overlay'
)
app.connect('activate', onActivate)
app.run(None)
