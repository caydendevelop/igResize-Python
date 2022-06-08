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


def not_4over5(width, height):
    ratio = width / height
    return ratio != 0.8


def is_vertical(width, height):
    return width < height


def add_margin(pil_img):
    width, height = pil_img.size
    if(is_vertical(width, height)):
        if(not_4over5(width, height)):
            left = right = int((height / 5 * 4 - width) / 2)
            new_width = width + left + right
            result = pil_image.new(
                pil_img.mode, (new_width, height), (255, 255, 255))
            result.paste(pil_img, (left, 0))
            return result
        else:
            return pil_img
    else:
        return pil_img


def entire_directory():

    directory_path = askdirectory()

    if (directory_path == ""):
        print("not chosen")
        return

    chosen_directory = os.listdir(directory_path)
    is_exist_output_directory = os.path.isdir(directory_path + "/output/")

    if(not is_exist_output_directory):
        os.makedirs(directory_path + "/output/")

    for i in chosen_directory:
        if (not i.endswith('.jpg') and not i.endswith('.jpeg') and not i.endswith('.png') and not i.endswith('.dng')):
            continue
        im = pil_image.open(directory_path + "/" + i)
        im_new = add_margin(im)

        output_path_and_filename = directory_path + "/output/" + i
        im_new.save(output_path_and_filename, quality=100)
        
    MyApp.show_success_msg("" , "Resize成功!")

def single_file():

    # show an "Open" dialog box and return the path to the selected file
    file_path = askopenfilename()

    if(file_path == ""):
        print("not chosen")
        return

    im = pil_image.open(file_path)
    filename = get_filename(file_path)
    dirname = get_dirname(file_path)
    im_new = add_margin(im)

    is_exist_output_directory = os.path.isdir(dirname + "/output/")

    if(not is_exist_output_directory):
        os.makedirs(dirname + "/output/")

    output_path_and_filename = dirname + "/output/" + filename
    im_new.save(output_path_and_filename, quality=100)
    MyApp.show_success_msg("" , "Resize成功!")

# Define a function to close the window
def close():
    quit()
   

class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title('Instagram Resize by Sofu')
        self.geometry('320x220')
        button1 = Button(self, text='選擇整個資料夾', command=entire_directory, padx=50, pady=15)
        button1.pack(pady=10)
        button2 = Button(self, text='選擇單張圖片', command=single_file, padx=56, pady=15)
        button2.pack(pady=10)
        button3 = Button(self, text='結束', command=close, padx=80, pady=15)
        button3.pack(pady=10)

    def show_success_msg(title, msg):
        tkinter.messagebox.showinfo(title, msg)

def gui_component():
    MyApp().mainloop()

def mainFunc():

    gui_component()

    # option = ""
    # while(option != "3"):

    #     option = input("""Enter your option: \n1 - Choosing Folder \n2 - Choosing Single Photo \n3 - Exit \n""")

    #     if(option == "3"):
    #         print("See you~ \n")
    #         break

    #     # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
        
    #     if(option == "1"):
    #         entire_directory()
    #         print("Done. Please check the output folder \n")
    #     if(option == "2"):
    #         single_file()
    #         print("Done. Please check folder you chose \n")


if __name__ == '__main__':
    mainFunc()
