import argparse
import sys
import os
import tkinter as tk
import PIL.Image
import PIL.ImageTk
from uploader import imgur
from screenshot import screenshot


def upload(filepath):
    print('Uploading screenshot')
    link = imgur.upload(filepath)
    print(link)

def take_screenshot(region=False, active=False, full=False):
    temp_file = "/tmp/temp.png"
    print("Taking Screenshot")
    screenshot.screenshot_active(temp_file)
    upload(temp_file)
    os.system('xclip -selection clipboard -t image/png -i {}'
              .format(temp_file))
    os.system('rm {}'.format(temp_file))

def start_gui():
    root = tk.Tk()
    temp_file = "/tmp/temp.png"
    screenshot.screenshot_full(temp_file)
    canvas_width = 1280
    canvas_height =720

    canvas = tk.Canvas(root, 
            width=canvas_width, 
            height=canvas_height)
    #canvas.pack(fill='both', expand='yes')
    canvas.pack()
    
    def resize(self, event):
        w,h = event.width-100, event.height-100
        self.canvas.config(width=w, height=h)
    
    canvas.bind('<Configure>', resize)


    temp_file = "/tmp/temp.png"
    img = tk.PhotoImage(file=temp_file)
    img = PIL.Image.open(temp_file)
    img = PIL.ImageTk.PhotoImage(img, PIL.Image.ANTIALIAS)
    # img.thumbnail(size, PIL.Image.ANTIALIAS)
    canvas.create_image(0, 0, anchor = 'nw', image = img)

    root.attributes('-type', 'dialog')
    root.mainloop()

class Example(tk.Frame):
    def __init__(self, master, *pargs):
        tk.Frame.__init__(self, master, *pargs)



        self.image = PIL.Image.open("/tmp/temp.png")
        self.img_copy= self.image.copy()


        self.background_image = PIL.ImageTk.PhotoImage(self.image)

        self.background = tk.Label(self, image=self.background_image)
        self.background.pack(fill='both', expand='yes')
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height
        new_image = self.img_copy.copy()
        #self.image = self.img_copy.resize((new_width, new_height))
        new_image.thumbnail((new_width, new_height), PIL.Image.ANTIALIAS)

        self.background_image = PIL.ImageTk.PhotoImage(new_image)
        self.background.configure(image =  self.background_image)


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
    args = vars(parser.parse_args())
    if args['region']:
        take_screenshot(region=True)
    elif args['active']:
        take_screenshot(active=True)
    elif args['full']:
        take_screenshot(full=True)
    else:
        temp_file = "/tmp/temp.png"
        screenshot.screenshot_full(temp_file)
        root = tk.Tk()
        root.title("Title")
        root.geometry("600x600")
        root.configure(background="black")
        root.attributes('-type', 'dialog')
        e = Example(root)
        e.pack(fill='both', expand='yes')
        root.mainloop() 
        