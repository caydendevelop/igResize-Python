import tkinter
from typing import Hashable
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


def add_margin(pil_img, option):
    width, height = pil_img.size
    if option == "vertical":
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

    elif option == "both":
        if is_vertical(width, height): # vertical
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
            top = bottom = int((width / 4 * 5 - height) / 2)
            new_height = height + top + bottom
            result = pil_image.new(
                pil_img.mode, (width, new_height), padding_color)
            result.paste(pil_img, (0, top))
            return result
        


def entire_directory(option):
    directory_path = askdirectory()

    if directory_path == "":
        return

    chosen_directory = os.listdir(directory_path)
    if len(chosen_directory) == 0:
        MyApp.show_msg("選擇的資料夾沒有檔案")

    is_exist_output_directory = os.path.isdir(directory_path + "/output/")

    if not is_exist_output_directory:
        os.makedirs(directory_path + "/output/")

    counter = 0
    for i in chosen_directory:
        
        if not i.endswith('.jpg') and not i.endswith('.jpeg') and not i.endswith('.png') and not i.endswith('.dng'):
            continue

        im = pil_image.open(directory_path + "/" + i)
        im_new = add_margin(im, option)
        output_path_and_filename = directory_path + "/output/" + i
        im_new.save(output_path_and_filename, quality=100)
        counter += 1

    MyApp.show_msg("", "Resize成功! 合共" + str(counter) + "張圖片")


def single_file(option):
    file_path = askopenfilename()

    if file_path == "":
        return

    im = pil_image.open(file_path)
    filename = get_filename(file_path)
    dirname = get_dirname(file_path)
    im_new = add_margin(im, option)

    is_exist_output_directory = os.path.isdir(dirname + "/output/")

    if not is_exist_output_directory:
        os.makedirs(dirname + "/output/")

    output_path_and_filename = dirname + "/output/" + filename
    im_new.save(output_path_and_filename, quality=100)
    MyApp.show_msg("", "Resize成功!")


# Define a function to close the window
def close():
    quit()


class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.title('Instagram Resize by Sofu')
        self.geometry('430x660')
        self.configure(background="#111415")

        frame1 = Frame(self)
        frame2 = Frame(self)
        frame1.configure(background="#111415")
        frame2.configure(background="#111415")

        self.button_white = Button(frame1, text='白邊', command=self.color_white, font=("Microsoft YaHei", 14), fg="#0a84ff", bg="#ffffff")
        self.button_white.grid(row=0, column=0, ipadx=8, padx=10)
        self.button_grey = Button(frame1, text='灰邊', command=self.color_grey, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button_grey.grid(row=0, column=1, ipadx=8, padx=10)
        self.button_black = Button(frame1, text='黑邊', command=self.color_black, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button_black.grid(row=0, column=2, ipadx=8, padx=10)

        self.button1 = Button(frame2, text='整個資料夾 (直+橫)', command=lambda: entire_directory('both'), padx=34, pady=15, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button1.pack(pady=10)
        self.button2 = Button(frame2, text='單張圖片 (直/橫)', command=lambda: single_file('both'), padx=52, pady=15, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button2.pack(pady=10)
        self.button3 = Button(frame2, text='整個資料夾 (直)', command=lambda: entire_directory('vertical'), padx=58, pady=15, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button3.pack(pady=10)
        self.button4 = Button(frame2, text='單張圖片 (直)', command=lambda: single_file('vertical'), padx=72, pady=15, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button4.pack(pady=10)
        self.button5 = Button(frame2, text='結束', command=close, padx=128, pady=15, font=("Microsoft YaHei", 14), fg="#ffffff", bg="#0A84FF")
        self.button5.pack(pady=10)

        frame1.pack(padx=5,pady=(20,10))
        frame2.pack(padx=5,pady=0)

    def reset_button_color(self):
        self.button_white.configure(fg="#ffffff", bg="#0a84ff")
        self.button_grey.configure(fg="#ffffff", bg="#0a84ff")
        self.button_black.configure(fg="#ffffff", bg="#0a84ff")

    def color_white(self):
        global padding_color
        padding_color = (255, 255, 255)
        self.reset_button_color()
        self.button_white.configure(fg="#0a84ff", bg="#ffffff")

    def color_grey(self):
        global padding_color
        padding_color = (127, 127, 127)
        self.reset_button_color()
        self.button_grey.configure(fg="#0a84ff", bg="#ffffff")

    def color_black(self):
        global padding_color
        padding_color = (0, 0, 0)
        self.reset_button_color()
        self.button_black.configure(fg="#0a84ff", bg="#ffffff")
        

    def show_msg(title, msg):
        tkinter.messagebox.showinfo(title, msg)


def main_func():
    MyApp().mainloop()

if __name__ == '__main__':
    main_func()
