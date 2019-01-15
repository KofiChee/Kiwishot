import sys
import os

from absl import app
from absl import flags
from kiwishot.uploader import imgur
from kiwishot.screenshot import screenshot

FLAGS = flags.FLAGS
flags.DEFINE_bool('region',
                  None,
                  'Take a screenshot of a selected region',
                  short_name='r'
                  )
flags.DEFINE_bool('active',
                  None,
                  'Take a screenshot of the active window',
                  short_name='a'
                  )
flags.DEFINE_bool('full',
                  None,
                  'Take a screenshot of the entire screen',
                  short_name='f'
                  )

flags.DEFINE_bool('upload',
                  False,
                  'Upload to image host',
                  short_name='u'
                  )

flags.DEFINE_string('save_location',
                    '/tmp/tmp.png',
                    'File to save screenshot to, default is /tmp/tmp.png',
                    short_name='s')

flags.mark_flags_as_mutual_exclusive(['region', 'active', 'full'])


def upload_image(filepath):
    """Uploads image to host and prints link to console"""
    print('Uploading screenshot')
    link = imgur.upload(filepath)
    print(link)


def take_screenshot(region=False, active=False,
                    full=False, upload=True):
    """Takes screenshot based on given flags.

    Also pushes image to clipboard using xclip.
    if gui is not set, it also uploads the image.
    """
    print("Taking Screenshot")
    if region:
        screenshot.screenshot_region(FLAGS.save_location)
    elif active:
        screenshot.screenshot_active(FLAGS.save_location)
    else:
        screenshot.screenshot_full(FLAGS.save_location)
    if upload:
        upload_image(FLAGS.save_location)

    os.system('xclip -selection clipboard -t image/png -i {}'
              .format(FLAGS.save_location))

def main(argv):
    del argv

    take_screenshot(FLAGS.region,
                    FLAGS.active,
                    FLAGS.full,
                    FLAGS.upload)

def run_main():
    app.run(main)

if __name__ == '__main__':
        app.run(main)
