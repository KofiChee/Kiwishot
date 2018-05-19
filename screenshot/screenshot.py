import sys
import os
from utils import xselect


def screenshot_full(filename):
    """Takes screenshot of entire root window (desktop)"""
    X = xselect.xselect()
    #TODO: Grab the root window dimensions
    image = X.grab_image(0, 0, 1920, 1080)
    image.save(filename)

def screenshot_active(filename):
    """Takes screenshot of active window
    
    use xdotool to find the id of active window
    """
    #command = 'import -window "$(xdotool getwindowfocus -f)" {}'
    #os.system(command.format(filename))
    X = xselect.xselect()
    coords = X.active_window()
    x = coords['x']                                                  
    y = coords['y']                                                  
    w = coords['width']                                              
    h = coords['height']                                             
    #command = 'import -window root -crop \'{}x{}+{}+{}\' {}'        
    #os.system(command.format(w, h, x, y, filename))                 
    image = X.grab_image(x, y, w, h)                                 
    image.save(filename) 


def screenshot_region(filename):
    """Take screenshot of selected region.

    Use our xselect class to draw a rectangle on screen and pass
    the coordinates into ImageMagick
    """
    X = xselect.xselect()
    coords = X.select_region()
    print(coords)
    x = coords['x']
    y = coords['y']
    w = coords['width']
    h = coords['height']
    #command = 'import -window root -crop \'{}x{}+{}+{}\' {}'
    #os.system(command.format(w, h, x, y, filename))
    image = X.grab_image(x, y, w, h)
    image.save(filename)
