import pyimgur

CLIENT_ID = "dcc1c15bae05fc3"

def upload(filepath):
    """
    Takes a filepath of an image and attempts to upload
    it to imgur.
        Arguments:
            filepath: String, filepath of image
        Returns:
            link: String, link to image on successful upload
    """
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(filepath)
    return uploaded_image.link