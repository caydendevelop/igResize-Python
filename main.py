from PIL import Image  # Python Image Library
from tkinter import Tk  # Python GUI library
from tkinter.filedialog import askdirectory  # Python GUI library to open the macOS finder
import os
from tkinter.filedialog import askopenfilename  # Python GUI library to open the macOS finder
from ntpath import basename as get_filename  # Python library using to get the filename from filepath


def not_4over5(width, height):
    ratio = width / height
    return ratio != 0.8

def is_vertical(width, height):
    return width < height

def add_margin(pil_img):
    width, height = pil_img.size
    if(is_vertical(width, height)):
        if(not_4over5(width, height)):
            left = right = int( (height / 5 * 4 - width) / 2)
            new_width = width + left + right
            result = Image.new(pil_img.mode, (new_width, height), (255, 255, 255))
            result.paste(pil_img, (left, 0))
            return result
        else:
            return pil_img
    else:
        return pil_img


def mainFunc():
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing

    ### Entire Directory
    directory_path = askdirectory()
    if(directory_path == ""):
        print("not chosen")
        return
    chosen_directory = os.listdir(directory_path)
    for i in chosen_directory:
        if(i.endswith('.DS_Store')):
            continue
        im = Image.open(directory_path + "/" + i)
        im_new = add_margin(im)
        output_path_and_filename = "./output/" + i
        print(output_path_and_filename)
        im_new.save(output_path_and_filename, quality=100)

    ### Single File
    # file_path = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    # if(file_path == ""):
    #     print("not chosen")
    #     return
    # im = Image.open(file_path)
    # filename = get_filename(file_path)
    # print("filename: " + filename)
    # im_new = add_margin(im)
    # output_path_and_filename = "./output/" + filename
    # im_new.save(output_path_and_filename, quality=100)

if __name__ == '__main__':
    mainFunc()

