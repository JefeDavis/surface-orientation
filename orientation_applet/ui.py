import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk as gdk


THEME_DARK = "dark"
THEME_LIGHT = "light"


def _luminance(r, g, b, base=256):
	#Calculates luminance of a color, on a scale from 0 to 1, meaning that 1 is the highest luminance.
	#r, g, b arguments values should be in 0..256 limits, or base argument should define the upper limit otherwise
	return (0.2126*r + 0.7152*g + 0.0722*b)/base


def __pixel_at(x, y):
    #Returns (r, g, b) color code for a pixel with given coordinates (each value is in 0..256 limits)
    root_window = gdk.get_default_root_window()
    buf = gdk.pixbuf_get_from_window(root_window, x, y, 1, 1)
    pixels = buf.get_pixels()
    if type(pixels) == type(""):
        rgb = tuple([int(byte.encode('hex'), 16) for byte in pixels])[0:3]
    else:
        rgb = tuple(pixels)[0:3]
    return rgb

def _get_theme():
	#Returns one of THEME_LIGHT or THEME_DARK, corresponding to current user's UI theme
	# getting color of a pixel on a top bar, and identifying best-fitting color theme based on its luminance
	pixel_rgb = __pixel_at(2, 2)
	luminance = _luminance(*pixel_rgb)
	return THEME_LIGHT if luminance >= 0.5 else THEME_DARK


THEME = _get_theme()
