
from tkinter import Label, Button, filedialog

class Gui:

    def __init__(self, root):

        self.directory = None

        self.root = root

        self.root.title("Mass Exif Editor")

        self.label = Label(self.root, text="Choose a folder and then hit submit")
        self.label.pack()

        self.choose_button = Button(self.root, text="Choose folder", command=self.choose_file)
        self.choose_button.pack()

        self.close_button = Button(self.root, text="Close", command=self.root.quit)
        self.close_button.pack()

    def choose_file(self):
        print("yello")
        directory = filedialog.askdirectory(title="Pick a file")
        self.directory = directory


class Date:

    def __init__(self, day=None, month=None, year=None):
        self.day = day
        self.month = month
        self.year = year
