import os
import re
import piexif

from tkinter import Label, Button, filedialog
from pprint import pprint
from PIL import Image
from pathlib import Path


def decode_bytes(bytelist):
    """Decodes a list of UCS2 encoded bytes into a string"""
    result = ""

    for decimal in bytelist:
        if decimal != 0:
            result += chr(decimal)

    return result

def encode_string(string):
    """Returns a string encoded into 2-byte character codes"""
    result = []
    for char in string:
        result.append(ord(char))
        result.append(0)
    result.append(0)
    result.append(0)

    return result

def parse_date(string):
    """Parses date in a string, not sure what this should return yet"""
    pattern = "(january|february|march|april|may|june|july|august|september|october|november|december)\s*(\d{1,2})\s*,?\s* (\d+)"
    result = re.search(pattern, string, re.IGNORECASE)

    print(result)
    return result

def parse_time(string):
    pass



im = Image.open("C:/Users/Maro/Desktop/test/unnamed.jpg")
exif_dict = piexif.load(im.info["exif"])
exif_dict["0th"][piexif.ImageIFD.XPTitle] = encode_string("fdsf")
exif_dict["0th"][piexif.ImageIFD.ImageDescription] = b"fff"
exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = b"2012:12:12 16:00:00"
exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = b"2012:12:12 16:00:00"
exif_bytes = piexif.dump(exif_dict)
im.save("C:/Users/Maro/Desktop/test/unnamed.jpg", "JPEG", exif=exif_bytes)



class Gui:

    def __init__(self, root):

        self.directory = None

        self.root = root

        self.root.title("Mass Exif Editor")

        self.label = Label(self.root, text="Choose a folder and then hit submit")
        self.label.pack()

        self.choose_button = Button(self.root, text="Choose folder",
                                    command=self.choose_file)
        self.choose_button.pack()

        self.choose_button = Button(self.root, text="Run Tool",
                                    command=self.update_images)
        self.choose_button.pack()

        self.close_button = Button(self.root, text="Quit",
                                   command=self.root.quit)
        self.close_button.pack()

    def choose_file(self):

        self.directory = filedialog.askdirectory(title="Pick a file")
        print("Selected", self.directory)

    def update_images(self):

        # **** TESTING PURPOSES **** - DELETE AFTER
        if self.directory is None:
            self.directory = "C:/Users/Maro/Desktop/test"

        files = os.listdir(self.directory)

        for file in files:
            filepath = Path(self.directory) / file
            im = Image.open(filepath)
            exif_dict = piexif.load(im.info["exif"])

            title_field = file.split(".", 1)[0]
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = title_field

            comment_field = decode_bytes(exif_dict["0th"][piexif.ImageIFD.XPComment]).strip()

            if comment_field:
                date_string = parse_date(comment_field)
                time_string = parse_time(comment_field)

                datetime = date_string + " " + time_string
                exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime

            exif_bytes = piexif.dump(exif_dict)
            im.save(filepath, "JPEG", exif=exif_bytes)

class Date:

    def __init__(self, day=None, month=None, year=None):
        self.day = day
        self.month = month
        self.year = year
