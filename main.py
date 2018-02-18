import sys
from uploader import imgur

def screenshot():
    filepath = sys.argv[1]
    link = imgur.upload(filepath)
    print(link)


if __name__ == '__main__':
    screenshot()
