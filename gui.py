import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from upscaler import upscale_file

# try:
#     from upscaler import file_is_valid
# except AssertionError as e:
#     messagebox.showinfo("Torch error", e)
#     exit(0)


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("ESRGan Upscaler")
        self.minsize(640, 400)
        # self.wm_iconbitmap('icon.ico')

        # label frame for selection buttons
        self.labelFrameButton = ttk.LabelFrame(self, text="Select image(s)")
        self.labelFrameButton.grid(column=0, row=1, padx=20, pady=20)

        self.fileButton = self.openFileButton()
        # self.dirButton = self.openDirButton()

        self.selectionLabel = ttk.Label(self.labelFrameButton, text="")
        self.selectionLabel.grid(column=1, row=3)

        self.goButton = self.goButton()

    def openFileButton(self):
        button = ttk.Button(self.labelFrameButton,
                            text="Select an image", command=self.fileDialog)
        button.grid(column=1, row=1)
        return button

    def openDirButton(self):
        button = ttk.Button(self.labelFrameButton,
                            text="Select directory", command=self.dirDialog)
        button.grid(column=1, row=2)
        return button

    def goButton(self):
        button = ttk.Button(self.labelFrameButton,
                            text="Start upscaling!", command=self.runUpscaling,
                            state="disabled")
        button.grid(column=1, row=4)
        return button

    def readyToUpscale(self, path):
        self.imagePath = path
        self.selectionLabel.configure(text=os.path.basename(path))
        self.selectionLabel.grid(column=1, row=3)
        self.goButton.config(state='normal')

    def runUpscaling(self):
        upscale_file(self.imagePath)


    def fileDialog(self):
        path = filedialog.askopenfilename(initialdir="/home/fablab-ubuntu", title="Select A File",
                                                   filetypes=(("JPEG", "*.jpg *.jpeg"), ("PNG", "*.png")))
        self.readyToUpscale(path)

    def dirDialog(self):
        path = filedialog.askdirectory(
            initialdir="/", title="Select A File")
        self.readyToUpscale(path)


root = Root()
root.mainloop()

