import os
import re
import exifread

from tkinter import Tk
from pprint import pprint
from pathlib import Path

from modules import Date, Gui







def get_exif_tag(file, key):

    result = ""

    tags = exifread.process_file(file)

    if key in tags.keys():
        result = tags[key]

    return result


def get_exif_comment(file):

    key = "Image XPComment"
    comment = ""

    tag = get_exif_tag(file, key)

    if hasattr(tag, "values"):
        # Iterate all characters in the tag
        for char_as_decimal in tag.values:

            # Find only non-zero characters
            if char_as_decimal != 0:
                comment += chr(char_as_decimal)

    return comment

def parse_date(string):
    pattern = "(january|february|march|april|may|june|july|august|september|october|november|december)\s*(\d{1,2})\s*,?\s* (\d+)"
    result = re.search(pattern, string, re.IGNORECASE)

    return result


if __name__ == "__main__":

    root = Tk()
    gui = Gui(root)
    gui.root.mainloop()

    basepath = "C:/Users/Maro/Desktop/test"
    files = os.listdir(basepath)

    for file in files:
        filepath = Path(basepath) / file
        with open(filepath) as f:
            comment = get_exif_comment(filepath).strip()
            if comment != "":
                print(parse_date(comment).group(0))
















