import sys
import os
from utils import xselect


def screenshot_full(filename):
    os.system('import -window root {}'.format(filename))


def screenshot_active(filename):
    # use xdotool to find the id of active window
    command = 'import -window "$(xdotool getwindowfocus -f)" {}'
    os.system(command.format(filename))


def screenshot_region(filename):
    X = xselect.xselect()
    coords = X.select_region()
    x_off = coords['start']['x']
    y_off = coords['start']['y']
    x = coords['width']
    y = coords['height']
    command = 'import -window root -crop \'{}x{}+{}+{}\' {}'
    os.system(command.format(x, y, x_off, y_off, filename))
