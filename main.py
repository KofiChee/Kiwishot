import argparse
import sys
import os
from uploader import imgur
from screenshot import screenshot


def upload(filepath):
    print('Uploading screenshot')
    link = imgur.upload(filepath)
    print(link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrotum')
    parser.add_argument('-r', '--region',
                        help='Description for region argument',
                        action='store_true')
    parser.add_argument('-a', '--active',
                        help='Description for active argument',
                        action='store_true')
    args = vars(parser.parse_args())
    temp_file = "/tmp/temp.png"
    print("Taking Screenshot")
    print(args)
    if args['region']:
        screenshot.screenshot_region(temp_file)
    elif args['active']:
        screenshot.screenshot_active(temp_file)
    else:
        screenshot.screenshot_full(temp_file)
    upload(temp_file)
    os.system('xclip -selection clipboard -t image/png -i {}'
              .format(temp_file))
    os.system('rm {}'.format(temp_file))
