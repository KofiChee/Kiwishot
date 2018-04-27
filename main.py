import sys
import os
import tkinter as tk
import time
import PIL.Image
import PIL.ImageTk

from absl import app
from absl import flags
from uploader import imgur
from screenshot import screenshot

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

flags.DEFINE_bool('nogui',
                  None,
                  'Don\'t use the GUI, automatically uploads to image host',
                  short_name='ng'
                  )

flags.DEFINE_string('save_location',
                    '/tmp/tmp.png',
                    'File to save screenshot to, default is /tmp/tmp.png',
                    short_name='s')

flags.mark_flags_as_mutual_exclusive(['region', 'active', 'full'])


def upload(filepath):
    print('Uploading screenshot')
    link = imgur.upload(filepath)
    print(link)


def take_screenshot(region=False, active=False,
                    full=False, nogui=False):
    print("Taking Screenshot")
    if region:
        screenshot.screenshot_region(FLAGS.save_location)
    elif active:
        screenshot.screenshot_active(FLAGS.save_location)
    else:
        screenshot.screenshot_full(FLAGS.save_location)
    if nogui:
        upload(FLAGS.save_location)
        os.system('xclip -selection clipboard -t image/png -i {}'
                  .format(FLAGS.save_location))


class Gui(tk.Frame):
    def __init__(self, master, imagepath, *pargs):
        tk.Frame.__init__(self, master, *pargs)

        self.imagepath = imagepath

        self.image = PIL.Image.open(self.imagepath)
        self.background_image = PIL.ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image)

        self.background.pack(fill='both', expand='yes')
        self.background.bind('<Configure>', self._resize_image)

        self.button_frame = tk.Frame(master)
        self.full = tk.Button(self.button_frame,
                              text="Full Screen",
                              command=self._full)
        self.active = tk.Button(self.button_frame,
                                text="Active Window",
                                command=self._active)
        self.region = tk.Button(self.button_frame,
                                text="Region Select",
                                command=self._region)
        self.upload = tk.Button(self.button_frame,
                                text="Upload to Imgur",
                                command=self._upload)

        self.upload.pack(side='bottom')
        self.full.pack(side='left')
        self.active.pack(side='left')
        self.region.pack(side='left')
        self.button_frame.pack(side='bottom')

    def _upload(self):
        upload(self.imagepath)

    def _set_image(self):
        self.image = PIL.Image.open(self.imagepath)
        self._resize_image()
        # self.background_image = PIL.ImageTk.PhotoImage(self.image)
        # self.background.configure(image=self.background_image)

    def _full(self):
        self.master.withdraw()
        time.sleep(0.5)
        screenshot.screenshot_full(self.imagepath)
        self._set_image()
        self.master.deiconify()

    def _active(self):
        self.master.withdraw()
        screenshot.screenshot_active(self.imagepath)
        self._set_image()
        self.master.deiconify()

    def _region(self):
        self.master.withdraw()
        screenshot.screenshot_region(self.imagepath)
        self._set_image()
        self.master.deiconify()

    def _resize_image(self, event=None):
        if event:
            new_width = event.width
            new_height = event.height
        else:
            new_width = self.winfo_width()
            new_height = self.winfo_height()
        new_image = self.image.copy()
        # self.image = self.img_copy.resize((new_width, new_height))
        new_image.thumbnail((new_width, new_height), PIL.Image.ANTIALIAS)

        self.background_image = PIL.ImageTk.PhotoImage(new_image)
        self.background.configure(image=self.background_image)

    def _hide_window(self):
        self.master.withdraw()
        time.sleep(5)
        self.master.deiconify()


def main(argv):
    del(argv)

    take_screenshot(FLAGS.region,
                    FLAGS.active,
                    FLAGS.full,
                    FLAGS.nogui)

    if not FLAGS.nogui:
        root = tk.Tk()
        root.title("Title")
        root.geometry("600x600")
        root.configure(background="black")
        root.attributes('-type', 'dialog')
        e = Gui(root, FLAGS.save_location)
        e.pack(fill='both', expand='yes')
        root.mainloop()

if __name__ == '__main__':
    app.run(main)
