import sys
import os
from uploader import imgur
from screenshot import screenshot

def upload(filepath):
    print('Uploading screenshot...')
    link = imgur.upload(filepath)
    print(link)


if __name__ == '__main__':
    temp_file = "/tmp/temp.png"
    screenshot.screenshot_active()
    upload(temp_file)
    os.system('rm {}'.format(temp_file))
