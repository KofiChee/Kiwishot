import argparse
import sys
import os
import tkinter as tk
import time
import PIL.Image
import PIL.ImageTk
from uploader import imgur
from screenshot import screenshot


def upload(filepath):
    print('Uploading screenshot')
    link = imgur.upload(filepath)
    print(link)


def take_screenshot(region=False, active=False,
                    full=False, nogui=False):
    temp_file = "/tmp/temp.png"
    print("Taking Screenshot")
    if region:
        screenshot.screenshot_region(temp_file)
    elif active:
        screenshot.screenshot_active(temp_file)
    else:
        screenshot.screenshot_full(temp_file)
    if nogui:
        upload(temp_file)
        os.system('xclip -selection clipboard -t image/png -i {}'
                  .format(temp_file))
        os.system('rm {}'.format(temp_file))


def start_gui():
    temp_file = "/tmp/temp.png"
    screenshot.screenshot_active(temp_file)
    root = tk.Tk()
    root.title("Title")
    root.geometry("600x600")
    root.configure(background="black")
    root.attributes('-type', 'dialog')
    e = Gui(root, temp_file)
    e.pack(fill='both', expand='yes')
    root.mainloop()
    root.withdraw()


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
        print('WHY THOUGH')
        upload(self.imagepath)

    def _set_image(self):
        self.image = PIL.Image.open(self.imagepath)
        self._resize_image()
        # self.background_image = PIL.ImageTk.PhotoImage(self.image)
        # self.background.configure(image=self.background_image)

    def _full(self):
        root.withdraw()
        time.sleep(0.5)
        screenshot.screenshot_full(self.imagepath)
        self._set_image()
        root.deiconify()

    def _active(self):
        root.withdraw()
        screenshot.screenshot_active(self.imagepath)
        self._set_image()
        root.deiconify()

    def _region(self):
        root.withdraw()
        screenshot.screenshot_region(self.imagepath)
        self._set_image()
        root.deiconify()

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
        root.withdraw()
        time.sleep(5)
        root.deiconify()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrotum')
    parser.add_argument('-r', '--region',
                        help='Description for region argument',
                        action='store_true')
    parser.add_argument('-a', '--active',
                        help='Description for active argument',
                        action='store_true')
    parser.add_argument('-f', '--full',
                        help='Description for whole argument',
                        action='store_true')
    parser.add_argument('-n', '--nogui',
                        help='Don\'t run the GUI',
                        action='store_true')
    args = vars(parser.parse_args())
    if args['nogui']:
        take_screenshot(args['region'], args['active'],
                        args['full'], args['no-gui'])
    else:
        temp_file = "/tmp/temp.png"
        screenshot.screenshot_active(temp_file)
        root = tk.Tk()
        root.title("Title")
        root.geometry("600x600")
        root.configure(background="black")
        root.attributes('-type', 'dialog')
        e = Gui(root, temp_file)
        e.pack(fill='both', expand='yes')
        root.mainloop()
