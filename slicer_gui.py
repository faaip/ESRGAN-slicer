import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
from upscaler import upscale_file, upscale_directory


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("ESRGan Upscaler")
        # self.minsize(640, 400)
        # self.wm_iconbitmap('icon.ico')

        # label frame for selection buttons
        self.inputFrame = ttk.LabelFrame(self, text="Select image(s):")
        self.inputFrame.grid(column=0, row=1, padx=20, pady=20)

        self.outputFrame = ttk.LabelFrame(self, text="Select output:")
        self.outputFrame.grid(column=0, row=2, padx=20, pady=20)

        self.fileButton = self.openFileButton()
        self.dirButton = self.openDirButton()
        self.outputButton = self.outputBotton()

        self.selectionLabel = ttk.Label(self.inputFrame, text="")
        self.selectionLabel.grid(column=1, row=3)

        self.goButton = self.goButton()

    def openFileButton(self):
        button = ttk.Button(self.inputFrame,
                            text="Select an image", command=self.fileDialog)
        button.grid(column=1, row=1)
        return button

    def openDirButton(self):
        button = ttk.Button(self.inputFrame,
                            text="Select directory", command=self.dirDialog)
        button.grid(column=1, row=2)
        return button

    def outputBotton(self):
        button = ttk.Button(self.outputFrame,
                            text="Select output", state='disabled',
                            command=self.outputDialog)
        button.grid(column=1, row=4)
        return button

    def goButton(self):
        button = ttk.Button(self.outputFrame,
                            text="Start upscaling!", command=self.runUpscaling,
                            state="disabled")
        button.grid(column=1, row=5)
        return button

    def readyToUpscale(self, path):
        self.input_path = path
        self.selectionLabel.configure(text=os.path.basename(self.input_path))
        self.selectionLabel.grid(column=1, row=3)
        self.outputButton.config(state='normal')

    def outputDialog(self):
        if os.path.isfile(self.input_path):
            files = [('JPEG', '*.jpg'),
                     ('PNG', '*.png')]
            self.output_path = filedialog.asksaveasfilename(title='Save upscaled image as...', initialdir=os.path.dirname(self.input_path),
                                                            filetypes=files, defaultextension=files)
            self.goButton.config(state='normal')
        elif os.path.isdir(self.input_path):
            self.output_path = filedialog.askdirectory(title='Select output directory',initialdir=os.path.dirname(self.input_path))
            if os.path.isdir(self.output_path):
                if os.path.samefile(str(self.input_path), str(self.output_path)):
                    messagebox.showwarning("Warning", "Output directory cannot be the same as input")
            self.goButton.config(state='normal')

    def runUpscaling(self):
        if os.path.isfile(self.input_path):
            upscale_file(self.input_path, self.output_path)
        elif os.path.isdir(self.input_path):
            upscale_directory(self.input_path, self.output_path)

    def fileDialog(self):
        path = filedialog.askopenfilename(title='Select input file...', initialdir="/home/fablab-ubuntu", title="Select A File",
                                          filetypes=(("JPEG", "*.jpg *.jpeg"), ("PNG", "*.png")))
        self.readyToUpscale(path)

    def dirDialog(self):
        path = filedialog.askdirectory(
            initialdir="/", title="Select directory with images...")
        self.readyToUpscale(path)


if __name__ == '__main__':
    root = Root()
    root.mainloop()
