import customtkinter as ctk
import sys
import ast

from tkinter.filedialog import askopenfile



sys.path.append(r"C:\Users\seanl\AppData\Local\Programs\Python\Python311\Lib\site-packages")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def openFile():
    file = askopenfile(mode ='r', filetypes =[('Python Files', '*.txt')])
    if file is not None:
        filepath = file.name
        with open(filepath, "r") as f:
            content = f.read()
            new = ast.literal_eval(content)
            print(new)
            print(type(new))



root = ctk.CTk()
root.geometry("700x500")
root.title("Upload Test")

frame1 = ctk.CTkFrame(root,
                      width = 700,
                      height = 500)
frame1.grid(row = 0, column = 0)

button1 = ctk.CTkButton(frame1, 
                        width = 100, 
                        height = 50,
                        command = openFile)
button1.grid(row = 0, column = 0)








root.mainloop()