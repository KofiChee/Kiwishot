import sys
import os
from utils import xselect

def screenshot_active(filename):
    # use xdotool to find the id of active window
    os.system('import -window "$(xdotool getwindowfocus -f)" {}'.format(filename))

def screenshot_region(filename):
    X = xselect.xselect()
    coords = X.select_region()
    x_off = coords['start']['x']
    y_off = coords['start']['y']
    x = coords['width']
    y = coords['height']
    os.system('import -window root -crop \'{}x{}+{}+{}\' {}'.format(x, y, x_off, y_off, filename))
