import sys
import os
from kiwishot.utils import xselect


def screenshot_full(filename):
    """Takes screenshot of entire root window (desktop)"""
    X = xselect.xselect()
    dimensions = X.fullscreen()
    image = X.grab_image(0, 0, dimensions['width'],
                         dimensions['height'])
    image.save(filename)


def screenshot_active(filename):
    """Takes screenshot of active window"""
    X = xselect.xselect()
    coords = X.active_window()

    x = coords['x']
    y = coords['y']
    w = coords['width']
    h = coords['height']

    image = X.grab_image(x, y, w, h)
    image.save(filename)


def screenshot_region(filename):
    """Take screenshot of selected region.

    Use our xselect class to draw a rectangle on screen and pass
    the coordinates into ImageMagick
    """
    X = xselect.xselect()
    coords = X.select_region()

    x = coords['x']
    y = coords['y']
    w = coords['width']
    h = coords['height']

    image = X.grab_image(x, y, w, h)
    image.save(filename)
