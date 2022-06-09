from ast import And
import tkinter
from PIL import Image as pil_image  # Python Image Library
from tkinter import *  # Python GUI library
# Python GUI library to open the macOS finder
from tkinter.filedialog import askdirectory
import os
# Python GUI library to open the macOS finder
from tkinter.filedialog import askopenfilename
# Python library using to get the filename from filepath
from ntpath import basename as get_filename
from ntpath import dirname as get_dirname

global padding_color  # global color
padding_color = (255, 255, 255)


def not_4over5(width, height):
    ratio = width / height
    return ratio != 0.8


def is_vertical(width, height):
    return width < height


def add_margin(pil_img):
    width, height = pil_img.size
    if is_vertical(width, height):
        if not_4over5(width, height):
            left = right = int((height / 5 * 4 - width) / 2)
            new_width = width + left + right
            result = pil_image.new(
                pil_img.mode, (new_width, height), padding_color)
            result.paste(pil_img, (left, 0))
            return result
        else:
            return pil_img
    else:
        return pil_img


def entire_directory():
    directory_path = askdirectory()

    if directory_path == "":
        return

    chosen_directory = os.listdir(directory_path)
    if len(chosen_directory) == 0:
        MyApp.show_msg("選擇的資料夾沒有檔案")

    is_exist_output_directory = os.path.isdir(directory_path + "/output/")

    if not is_exist_output_directory:
        os.makedirs(directory_path + "/output/")

    for i in chosen_directory:
        counter = 0
        if not i.endswith('.jpg') and not i.endswith('.jpeg') and not i.endswith('.png') and not i.endswith('.dng'):
            continue

        im = pil_image.open(directory_path + "/" + i)
        im_new = add_margin(im)
        output_path_and_filename = directory_path + "/output/" + i
        im_new.save(output_path_and_filename, quality=100)
        counter += 1

    MyApp.show_msg("", "Resize成功! 合共" + counter + "張圖片")


def single_file():
    file_path = askopenfilename()

    if file_path == "":
        return

    im = pil_image.open(file_path)
    filename = get_filename(file_path)
    dirname = get_dirname(file_path)
    im_new = add_margin(im)

    is_exist_output_directory = os.path.isdir(dirname + "/output/")

    if not is_exist_output_directory:
        os.makedirs(dirname + "/output/")

    output_path_and_filename = dirname + "/output/" + filename
    im_new.save(output_path_and_filename, quality=100)
    MyApp.show_msg("", "Resize成功!")


# Define a function to close the window
def close():
    quit()


def color_selector(color):
    if (color == "white"):
        padding_color = (255, 255, 255)
    elif (color == "grey"):
        padding_color = (127, 127, 127)
    elif (color == "black"):
        padding_color = (0, 0, 0)


class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title('Instagram Resize by Sofu')
        self.geometry('320x260')

        frame1 = Frame(self)
        frame2 = Frame(self)

        button_white = Button(frame1, text='白邊', command=lambda: color_selector("white"))
        button_white.grid(row=0, column=0)
        button_grey = Button(frame1, text='灰邊', command=lambda: color_selector("grey"))
        button_grey.grid(row=0, column=1)
        button_black = Button(frame1, text='黑邊', command=lambda: color_selector("black"))
        button_black.grid(row=0, column=2)

        button1 = Button(frame2, text='選擇整個資料夾', command=entire_directory, padx=50, pady=15)
        button1.pack(pady=10)
        button2 = Button(frame2, text='選擇單張圖片', command=single_file, padx=56, pady=15)
        button2.pack(pady=10)
        button3 = Button(frame2, text='結束', command=close, padx=80, pady=15)
        button3.pack(pady=10)

        frame1.pack(padx=5,pady=5)
        frame2.pack(padx=5,pady=5)

    def show_msg(title, msg):
        tkinter.messagebox.showinfo(title, msg)


def mainFunc():
    MyApp().mainloop()


if __name__ == '__main__':
    mainFunc()
