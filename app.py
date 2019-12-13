import os
import re
import piexif

from tkinter import Tk, Label, Button, Checkbutton, IntVar, filedialog
from tkinter.ttk import Progressbar

from pprint import pprint
from PIL import Image
from pathlib import Path

# TODO: Find a better place for these, maybe in the Date class
REGULAR_DATE = re.compile("(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})\s*,?\s*(\\b\d{4}\\b)",
                          flags=re.IGNORECASE)

REGULAR_CONDENSED = re.compile("\\b(\d{1,2})/(\d{1,2})/(\d{4})\\b",
                               flags=re.IGNORECASE)

MONTH_YEAR = re.compile("(january|february|march|april|may|june|july|august|september|october|november|december)\s*,?\s*(\\b\d{4}\\b)",
                        flags=re.IGNORECASE)

YEAR = re.compile("\\b\d{4}\\b",
                  flags=re.IGNORECASE)


TIME = re.compile("\\b(\d{1,2})\\b:(\d{1,2})\s*(a\\.?m\\.?|p\\.?m\\.?)",
                  flags=re.IGNORECASE)


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


def parse_date(string, **kwargs):
    """Attempts to match a date pattern in a string, returns Date object"""

    date = Date()

    result = REGULAR_DATE.search(string)
    if result:
        date.month = result.group(1)
        date.day = result.group(2)
        date.year = result.group(3)
        return date

    result = REGULAR_CONDENSED.search(string)
    if result:
        date.month = result.group(1)
        date.day = result.group(2)
        date.year = result.group(3)
        return date

    if "ignoreincomplete" in kwargs:
        ignoreincomplete = bool(kwargs.get("ignoreincomplete"))

        if ignoreincomplete:
            return date

    result = MONTH_YEAR.search(string)
    if result:
        date.month = result.group(1)
        date.day = "1"
        date.year = result.group(2)
        return date

    result = YEAR.search(string)
    if result:
        date.month = "1"
        date.day = "1"
        date.year = result.group(0)
        return date

    return date


def parse_time(string):
    """Attempts to match a time pattern in a string, returns Time object"""
    time = Time()

    result = TIME.search(string)
    if result:
        time.hour = result.group(1)
        time.minute = result.group(2)
        am = result.group(3).replace(".", "").lower().strip()
        if am == "am":
            time.am = True
        else:
            time.am = False

    return time

def rebuild_exif_structure(img_obj):
    img_obj.info["exif"] = {}
    img_obj.info["exif"]["0th"] = {}

class Gui:

    def __init__(self, root):

        # Other variables
        self.directory = None

        # GUI variables
        self.root = root
        self.root.title("Mass Exif Editor")

        self.help_text = Label(self.root, text="Choose a folder and then hit run")
        self.help_text.pack()

        self.path_label = Label(self.root, text="")
        self.path_label.pack()

        self.folder_button = Button(self.root, text="Choose folder",
                                    command=self.choose_file)
        self.folder_button.pack()

        self.ignoreincomplete = IntVar()
        self.ignore_checkbox = Checkbutton(self.root, text="Ignore incomplete dates",
                                           variable=self.ignoreincomplete)
        self.ignore_checkbox.pack()

        self.progress_bar = Progressbar(self.root, orient="horizontal",
                                        mode="determinate")
        self.progress_bar.pack(pady=10)

        self.run_button = Button(self.root, text="Run Tool",
                                 command=self.update_images)
        self.run_button.pack()

        self.close_button = Button(self.root, text="Quit",
                                   command=self.root.quit)
        self.close_button.pack()

    def choose_file(self):
        self.directory = filedialog.askdirectory(title="Choose folder")
        self.path_label["text"] = self.directory
        self.progress_bar["value"] = 0

    def update_images(self):

        if self.directory is None:
            return

        files = os.listdir(self.directory)

        self.progress_bar.length = len(files)
        self.progress_bar["value"] = 0
        self.root.update_idletasks()

        for file in files:

            self.progress_bar["value"] += (100 / self.progress_bar.length)
            self.root.update_idletasks()

            filepath = Path(self.directory) / file
            im = Image.open(filepath)

            if im.format != "JPEG" or "exif" not in im.info.keys():
                continue

            print(im.filename)
            exif_dict = piexif.load(im.info["exif"])

            title_field = file.split(".", 1)[0]
            exif_dict["0th"][piexif.ImageIFD.ImageDescription] = title_field

            if str(piexif.ImageIFD.XPComment) not in exif_dict["0th"].keys():
                comment_field = decode_bytes(exif_dict["0th"][piexif.ImageIFD.XPComment]).strip()

                if comment_field:
                    print("running")
                    date_string = str(parse_date(comment_field, ignoreincomplete=self.ignoreincomplete.get()))

                    if not date_string:
                        continue

                    time_string = str(parse_time(comment_field))

                    datetime = date_string + " " + time_string
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal] = datetime
                    exif_dict["Exif"][piexif.ExifIFD.DateTimeDigitized] = datetime

            exif_bytes = piexif.dump(exif_dict)
            im.save(filepath, "JPEG", exif=exif_bytes)



class Time:

    def __init__(self, hour="00", minute="00", second="00", am=True):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.am = am

    def __str__(self):

        string = ""

        hour_as_int = int(self.hour)

        # AM
        if self.am is False:
            if hour_as_int < 12:
                hour_as_int += 12
        # PM
        else:
            if hour_as_int == 12:
                hour_as_int = 0

        string += self.normalize_field(hour_as_int)

        string += ":" + self.minute + ":" + self.second

        return string


    def normalize_field(self, field):

        field = str(field)
        normalized_field = ""

        if len(field) < 2:
            normalized_field += "0" + field
        else:
            normalized_field = field

        return normalized_field


class Date:

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

    def __init__(self, day=None, month=None, year=None):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):

        if not self.year:
            return ""

        string = str(self.year) + ":"

        if self.month:

            # Convert any text month using the months dictionary
            if not self.month.isnumeric():
                self.month = self.MONTHS[self.month.lower().strip()]

            if len(self.month) < 2:
                string += "0"
            string += self.month
        else:
            string += "01"

        string += ":"

        if self.day:
            if len(self.day) < 2:
                string += "0"
            string += self.day
        else:
            string += "01"

        return string


if __name__ == "__main__":

    root = Tk()
    gui = Gui(root)
    gui.root.mainloop()
