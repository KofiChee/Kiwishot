import sys
import os
from utils import xselect

def screenshot_active(filename):
    # use xdotool to find the id of active window
    os.system('import -window "$(xdotool getwindowfocus -f)" {}'.format(filename))

def screenshot_region(filename):
    # X = xselect.xselect()
    # coords = X.select_region()
    # print(coords)
    # x = coords['start']['x']
    # y = coords['start']['y']
    # x_offset = coords['width']
    # y_offset = coords['height']
    # print(x, y, x_offset, y_offset)
    # os.system('import -crop {} {} {} {} {}'.format(x, y, x_offset, y_offset, filename))
    os.system('import {}'.format(filename))