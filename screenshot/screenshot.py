import sys
import os
from utils import xselect


def screenshot_full(filename):
    """Takes screenshot of entire root window (desktop)"""
    os.system('import -window root {}'.format(filename))


def screenshot_active(filename):
    """Takes screenshot of active window
    
    use xdotool to find the id of active window
    """
    command = 'import -window "$(xdotool getwindowfocus -f)" {}'
    os.system(command.format(filename))


def screenshot_region(filename):
    """Take screenshot of selected region.

    Use our xselect class to draw a rectangle on screen and pass
    the coordinates into ImageMagick
    """
    X = xselect.xselect()
    coords = X.select_region()
    x_off = coords['start']['x']
    y_off = coords['start']['y']
    x = coords['width']
    y = coords['height']
    command = 'import -window root -crop \'{}x{}+{}+{}\' {}'
    os.system(command.format(x, y, x_off, y_off, filename))
