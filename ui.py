from __future__ import division
from __future__ import print_function

import math
import subprocess
from itertools import groupby

import PIL.Image
import PIL.ImageTk
import numpy
import tkFileDialog
import ttk
from Tkinter import *

# instance for Tkinter
root = Tk()


class xBurnObject(object):
    filename = StringVar()
    width = IntVar()
    shades = IntVar()
    white_value = IntVar()
    x_density = DoubleVar()
    y_density = DoubleVar()
    palette_on = BooleanVar()
    skip_rate = IntVar()
    burn_rate = IntVar()
    steps = IntVar()
    max_power = IntVar()
    min_power = IntVar()
    laser_on = StringVar()
    laser_off = StringVar()
    laser_mod = StringVar()
    out_file_prefix = StringVar()
    preview_on = BooleanVar()
    debugging_on = BooleanVar()

    def __init__(self, filename, width, shades, white_values, x_density, y_density, palette_on, skip_rate, burn_rate,
                 steps,
                 max_power, min_power, laser_on, laser_off, laser_mod, out_file_prefix, preview_on, debugging_on):
        self.filename.set(filename)
        self.width.set(width)
        self.shades.set(shades)
        self.white_value.set(white_values)
        self.x_density.set(x_density)
        self.y_density.set(y_density)
        self.palette_on.set(palette_on)
        self.skip_rate.set(skip_rate)
        self.burn_rate.set(burn_rate)
        self.steps.set(steps)
        self.max_power.set(max_power)
        self.min_power.set(min_power)
        self.laser_on.set(laser_on)
        self.laser_off.set(laser_off)
        self.laser_mod.set(laser_mod)
        self.out_file_prefix.set(out_file_prefix)
        self.preview_on.set(preview_on)
        self.debugging_on.set(debugging_on)


class XBurnView:
    label1 = None
    img_path = ""
    xburn = xBurnObject(img_path, 50, 16, 255, 2.0, 2.0, True, 3000, 800, 255, 12000, 0, "M5", "M3", "S", "workfile",
                        True, True)

    def __init__(self, master):
        self.master = master
        # root.minsize(width=1024, height=768)
        root.title("xBurn")

        content = ttk.Frame(master, padding=(3, 3, 12, 12))
        content.grid(column=0, sticky=(N, S, E, W))

        # Frame 1 stuff
        frame1 = Frame(content, bg="grey", borderwidth=5, relief="sunken", width=512, height=768)
        frame1.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))

        # Image to burn vars
        iFrame = Frame(frame1, bg="yellow", borderwidth=5, relief="sunken", width=512)
        iFrame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))

        # Label(frame1, text="Number of shades", underline=True).grid(column=0, row=1, sticky=W, pady=5, padx=5)
        desired_width = Scale(iFrame, from_=0, to=500, length=300, label="Width to resize image in mm, defaults to 50",
                              orient=HORIZONTAL, variable=self.xburn.width)
        desired_width.grid(column=0, row=0, sticky=W, pady=5, padx=5)

        # Label(frame1, text="Number of shades", underline=True).grid(column=0, row=1, sticky=W, pady=5, padx=5)
        shades_num = Scale(iFrame, from_=1, to=257, length=300, label="Number of shades, defaults to 16",
                           orient=HORIZONTAL, variable=self.xburn.shades)
        shades_num.grid(column=0, row=1, sticky=W, pady=5, padx=5)

        # Label(frame1, text="White value", underline=True).grid(column=0, row=3, sticky=W, pady=5, padx=5)
        white_value = Scale(iFrame, from_=0, to=255, length=256, label="White value, defaults to 255",
                            orient=HORIZONTAL, variable=self.xburn.white_value)
        white_value.grid(column=1, row=1, sticky=E, pady=5, padx=5)

        # Label(frame1, text="x Density", underline=True).grid(column=0, row=5, sticky=W, pady=5, padx=5)
        x_density = Scale(iFrame, from_=0, to=10, length=256, resolution=0.1,
                          label="Pixels per mm in x direction, default 2.0", orient=HORIZONTAL,
                          variable=self.xburn.x_density)
        x_density.grid(column=0, row=2, sticky=W, pady=5, padx=5)

        # Label(frame1, text="y Density", underline=True).grid(column=0, row=7, sticky=W, pady=5, padx=5)
        y_density = Scale(iFrame, from_=0, to=10, length=256, resolution=0.1,
                          label="Pixels per mm in y direction, default 2.0", orient=HORIZONTAL,
                          variable=self.xburn.y_density)
        y_density.grid(column=1, row=2, sticky=E, pady=5, padx=5)

        palette = Checkbutton(iFrame, text="Palette", variable=self.xburn.palette_on)
        palette.grid(column=0, row=3, sticky=W, pady=5, padx=5)

        # Laser vars frame
        lFrame = Frame(frame1, bg="red", borderwidth=5, relief="sunken", width=512)
        lFrame.grid(column=0, row=2, columnspan=3, rowspan=2, sticky=(N, S, E, W))

        # Label(frame1, text="Skip rate", underline=True).grid(column=0, row=9, sticky=W, pady=5, padx=5)
        skip_rate = Scale(lFrame, from_=0, to=3000, length=256, label="Moving Feed Rate, defaults to 3000",
                          orient=HORIZONTAL, variable=self.xburn.skip_rate)
        skip_rate.grid(column=0, row=0, sticky=W, pady=5, padx=5)

        # Label(frame1, text="Burn rate", underline=True).grid(column=0, row=11, sticky=W, pady=5, padx=5)
        burn_rate = Scale(lFrame, from_=0, to=1000, length=256, label="Burning Feed Rate, defaults to 800",
                          orient=HORIZONTAL, variable=self.xburn.burn_rate)
        burn_rate.grid(column=1, row=0, sticky=W, pady=5, padx=5)

        # Label(frame1, text="Steps", underline=True).grid(column=0, row=13, sticky=W, pady=5, padx=5)
        steps = Scale(lFrame, from_=0, to=500, length=256, label="Laser PWM Steps, defaults to 255",
                      orient=HORIZONTAL, variable=self.xburn.steps)
        steps.grid(column=2, row=0, sticky=W, pady=5, padx=5)

        # Label(frame1, text="Max power", underline=True).grid(column=0, row=15, sticky=W, pady=5, padx=5)
        max_power = Scale(lFrame, from_=0, to=15000, length=300, label="Laser Max Power PWM VAlUE, defaults to 12000",
                          orient=HORIZONTAL, variable=self.xburn.max_power)
        max_power.grid(column=0, row=1, sticky=W, pady=5, padx=5)

        # Label(frame1, text="Min power", underline=True).grid(column=0, row=17, sticky=W, pady=5, padx=5)
        min_power = Scale(lFrame, from_=0, to=15000, length=300, label="Laser Min Power PWM VAlUE, defaults to 0",
                          orient=HORIZONTAL, variable=self.xburn.min_power)
        min_power.grid(column=1, row=1, sticky=E, pady=5, padx=5)

        Label(lFrame, text="Laser on command", underline=True).grid(column=0, row=2, sticky=W, pady=5, padx=5)
        laser_on = Entry(lFrame, width=20, textvariable=self.xburn.laser_on)
        laser_on.grid(column=0, row=3, sticky=W, pady=5, padx=5)

        Label(lFrame, text="Laser off command", underline=True).grid(column=1, row=2, sticky=W, pady=5, padx=5)
        laser_off = Entry(lFrame, width=20, textvariable=self.xburn.laser_off)
        laser_off.grid(column=1, row=3, sticky=W, pady=5, padx=5)

        Label(lFrame, text="Laser power modifier", underline=True).grid(column=2, row=2, sticky=W, pady=5, padx=5)
        laser_power_mod = Entry(lFrame, width=20, textvariable=self.xburn.laser_mod)
        laser_power_mod.grid(column=2, row=3, sticky=W, pady=5, padx=5)

        # Misc stuff
        mFrame = Frame(frame1, bg="blue", borderwidth=5, relief="sunken", width=512)
        mFrame.grid(column=0, row=4, columnspan=3, rowspan=2, sticky=(N, S, E, W))

        Label(mFrame, text="Outfile name", underline=True).grid(column=0, row=0, sticky=W, pady=5, padx=5)
        outfile_name = Entry(mFrame, width=50, textvariable=self.xburn.out_file_prefix)
        outfile_name.grid(column=0, row=1, sticky=W, pady=5, padx=5)

        check1 = Checkbutton(mFrame, text="Preview", variable=self.xburn.preview_on)
        check1.grid(column=2, row=0, sticky=W, pady=5, padx=5)

        check2 = Checkbutton(mFrame, text="Debug", variable=self.xburn.debugging_on)
        check2.grid(column=2, row=1, pady=5, padx=5)

        # Frame 2 stuff
        frame2 = Frame(content, bg="green", borderwidth=5, relief="sunken")
        frame2.grid(column=3, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))

        global label1
        label1 = Label(frame2, text="Upload image")
        label1.grid(row=0, column=0, sticky=N, pady=5, padx=5)
        # self.get_resize_update_img("mysterion.gif")

        button1 = Button(frame2, text="Upload image", width=20, command=self.upload_image)
        button1.grid(row=1, column=0, sticky=S, pady=5, padx=5)

        button2 = Button(frame2, text="Gradient test", width=20, command=self.gradient_test)
        button2.grid(row=2, column=0, sticky=S, pady=5, padx=5)

        button3 = Button(frame2, text="Convert image", width=20, command=self.convert_all)
        button3.grid(row=3, column=0, sticky=S, pady=5, padx=5)

        button4 = Button(frame2, text="Generate gcode", width=20, command=self.generate_gcode)
        button4.grid(row=4, column=0, sticky=S, pady=5, padx=5)

    def upload_image(self):
        global img_path
        img_path = tkFileDialog.askopenfilename()

        self.xburn.filename.set(img_path)

        self.get_resize_update_img(img_path)

    def generate_gcode(self):
        print('Width ' + str(self.xburn.width.get()))
        print('Shades ' + str(self.xburn.shades.get()))
        print('White value ' + str(self.xburn.white_value.get()))
        print('x density ' + str(self.xburn.x_density.get()))
        print('y density ' + str(self.xburn.y_density.get()))
        print('Density(max(x,y) ' + str(max(self.xburn.x_density.get(), self.xburn.y_density.get())))
        print('Skip rate ' + str(self.xburn.skip_rate.get()))
        print('Burn rate ' + str(self.xburn.burn_rate.get()))
        print('Steps ' + str(self.xburn.steps.get()))
        print('Max power ' + str(self.xburn.max_power.get()))
        print('Min power ' + str(self.xburn.min_power.get()))
        print('Laser on mapping ' + str(self.xburn.laser_on.get()))
        print('Laser off mapping ' + str(self.xburn.laser_off.get()))
        print('Laser mod ' + str(self.xburn.laser_mod.get()))
        print('Outfile prefix ' + str(self.xburn.out_file_prefix.get()))
        print('Preview ON ' + str(self.xburn.preview_on.get()))
        print('Debug ON ' + str(self.xburn.debugging_on.get()))

        # TODO replace with the proper calls
        # start cli process
        cmd = './cli.py ' + (self.xburn.filename.get() + ' ') \
              + (str(self.xburn.width.get()) + ' ') \
              + ('-s ' + str(self.xburn.shades.get()) + ' ') \
              + ('-wv ' + str(self.xburn.white_value.get()) + ' ') \
              + ('-de ' + str(max(self.xburn.x_density.get(), self.xburn.y_density.get())) + ' ') \
              + ('-sr ' + str(self.xburn.skip_rate.get()) + ' ') \
              + ('-br ' + str(self.xburn.burn_rate.get()) + ' ') \
              + ('-st ' + str(self.xburn.steps.get()) + ' ') \
              + ('-hp ' + str(self.xburn.max_power.get()) + ' ') \
              + ('-lp ' + str(self.xburn.min_power.get()) + ' ') \
              + ('-on ' + str(self.xburn.laser_on.get()) + ' ') \
              + ('-off ' + str(self.xburn.laser_off.get()) + ' ') \
              + ('-mod ' + str(self.xburn.laser_mod.get()) + ' ') \
              + ('-o ' + str(self.xburn.out_file_prefix.get()) + ' ') \
              + ('-p ' if self.xburn.preview_on.get() else '') \
              + ('-d ' if self.xburn.debugging_on.get() else '')

        print(cmd)

        subprocess.Popen(cmd, shell=True)

    def get_resize_update_img(self, path):
        global img_path
        img_path = path

        base_width = 400
        img = PIL.Image.open(img_path)
        [img_width, img_height] = img.size

        width_ratio = (base_width / float(img_width))
        new_height = int((float(img_height) * float(width_ratio)))

        img = img.resize((base_width, new_height), PIL.Image.ANTIALIAS)

        img2 = PIL.ImageTk.PhotoImage(img)
        label1.configure(image=img2)
        label1.image = img2

        return img

    def resize_update_img(self, image):
        base_width = 400
        img = image
        [img_width, img_height] = img.size

        width_ratio = (base_width / float(img_width))
        new_height = int((float(img_height) * float(width_ratio)))

        img = img.resize((base_width, new_height), PIL.Image.ANTIALIAS)

        img2 = PIL.ImageTk.PhotoImage(img)
        label1.configure(image=img2)
        label1.image = img2

        return img

    def convert_image(self):
        img = PIL.Image.open(img_path)
        [img_width, img_height] = img.size

        img = img.convert("L")

        height_ratio = self.xburn.width.get() / (img_width / img_height)
        resize_co = (int(math.floor(self.xburn.x_density.get() * self.xburn.width.get())),
                     int(math.floor(self.xburn.y_density.get() * height_ratio)))

        if self.xburn.palette_on.get():
            if self.xburn.shades.get() < 3:
                palette = [0, 0, 0, 255, 255, 255, ] + [255, ] * 254 * 3
            else:
                palette = [0, 0, 0, ]
                steps = int(math.floor(256 / (self.xburn.shades.get() - 1)))
                for c in range(self.xburn.shades.get() - 2):
                    m = c + 1
                    palette = palette + [steps * m, steps * m, steps * m]
                palette = palette + [255, ] * (256 - self.xburn.shades.get()) * 3

            pimage = PIL.Image.new("P", (1, 1), 0)
            pimage.putpalette(palette)

            img = img.quantize(colors=self.xburn.shades.get(), palette=pimage)

        img = img.resize(resize_co, PIL.Image.LANCZOS) \
            .transpose(PIL.Image.ROTATE_180) \
            .transpose(PIL.Image.FLIP_LEFT_RIGHT)

        # self.resize_update_img(img)

        return img

    def get_converted_img_array(self, img):
        return numpy.array(img)

    # creates a 255x20 black to white gradient for testing settings
    def gradient_test(self):
        test = PIL.Image.new('RGB', (255, 20), "black")  # create a new black image
        pixels = test.load()  # create the pixel map
        for i in range(test.size[0]):  # for every pixel:
            for j in range(test.size[1]):
                pixels[i, j] = (i, i, i)  # set the colour accordingly

        self.resize_update_img(test)

    def convert_all(self):
        img = self.convert_image()
        arr = self.get_converted_img_array(img)

        prv = PIL.Image.new('RGB', (len(arr[0]), len(arr)), "red")
        pixels = prv.load()  # create the pixel map

        # Y position
        yp = 0

        for y in arr:
            # If we have an even number for a y axis line
            if yp % 2 != 0:
                # Direction is reversed, set xp to the end
                xp = len(y) - 1
                # Revese the values of y
                y = list(reversed(y))
                rev = True
            else:
                xp = 0
                rev = False
            # Group pixels by value into a new list
            for i, j in groupby(y):
                # items in the list
                items = list(j)
                # Number of items
                size = len(items)
                # grey Value in this chunk of the line
                value = items[0]
                # Make sure this group isn't above the whitevalue
                if value < self.xburn.white_value.get():

                    pvx = len(items) - 1 if rev else 0
                    for item in items:
                        pix = xp - pvx if rev else xp + pvx
                        pixels[pix, yp] = (item, item, item)
                        pvx = pvx - 1 if rev else pvx + 1

                # Increment position
                xp = xp - size if rev else xp + size

            yp = yp + 1

        prv.transpose(PIL.Image.ROTATE_180).transpose(PIL.Image.FLIP_LEFT_RIGHT)

        self.resize_update_img(prv)


xburn = XBurnView(root)
root.mainloop()
