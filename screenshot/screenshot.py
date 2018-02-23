import os

def screenshot_active(filename):
    # use xdotool to find the id of active window
    os.system('import -window "$(xdotool getwindowfocus -f)" {}'.format(filename))