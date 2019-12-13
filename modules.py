import os
import re
import piexif

from tkinter import Label, Button, Checkbutton, IntVar, filedialog
from pprint import pprint
from PIL import Image
from pathlib import Path

MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}

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
    """Parse date, create a date object, return a normalized version"""

    date = Date()

    pattern = "(january|february|march|april|may|june|july|august|september|october|november|december)\s*(\d{1,2})\s*,?\s*(\d{4})"
    result = re.search(pattern, string, re.IGNORECASE)

    if result is not None:
        print("1")
        print(result)
        date.year = result.group(3)
        date.month = result.group(1)
        date.day = result.group(2)
        return date


    # Pattern matching month (space) year
    pattern = "(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{4})"
    result = re.search(pattern, string, re.IGNORECASE)

    if result is not None:
        print("2")
        print(result)
        date.year = result.group(2)
        date.month = result.group(1)
        date.day = "1"
        return date

    return result



def parse_time(string):
    pass


class Gui:

    def __init__(self, root):

        # Other variables
        self.directory = None

        # GUI variables
        self.root = root
        self.root.title("Mass Exif Editor")

        self.help_text = Label(self.root, text="Choose a folder and then hit run").grid(row=0)

        self.folder_button = Button(self.root, text="Choose folder",
                                    command=self.choose_file).grid(row=1, column=1, sticky="W")

        self.ignore_dates = IntVar()
        self.ignore_checkbox = Checkbutton(self.root, text="Ignore incomplete dates",
                                           variable=self.ignore_dates).grid(row=2, column=1, sticky="W")

        self.run_button = Button(self.root, text="Run Tool",
                                 command=self.update_images).grid(row=3, column=1, sticky="W")

        self.close_button = Button(self.root, text="Quit",
                                   command=self.root.quit).grid(row=3, column=0, sticky="W")

    def choose_file(self):
        self.directory = filedialog.askdirectory(title="Pick a file")

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
                exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = datetime

            exif_bytes = piexif.dump(exif_dict)
            im.save(filepath, "JPEG", exif=exif_bytes)

class Date:

    def __init__(self, day=None, month=None, year=None):
        self.day = day
        self.month = month
        self.year = year

parse_date("january 1, 2015ff")
"""
im = Image.open("C:/Users/Maro/Desktop/test/unnamed.jpg")
exif_dict = piexif.load(im.info["exif"])
print(exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal])
print(exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized])
"""