# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 13:47:28 2022

@author: seanl
"""

import sys
sys.path.append(r"C:\Users\seanl\AppData\Local\Programs\Python\Python311\Lib\site-packages")


import customtkinter as ctk


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def startProgressBar(bar, button):
    bar.start()
    button.configure(text = "Stop", 
                     command= lambda: stopProgressBar(bar, button) )
def stopProgressBar(bar, button):
    bar.stop()
    button.configure(text = "Start",
                     command = lambda: startProgressBar(bar, button))

def switcher(holder):
    if holder.get():
        print("On")
    else:
        print("Off")
        
def sliderFun(value):
    print(value)
    
def dialogueFun():
    dialogue = ctk.CTkInputDialog(text = "Enter something",
                                  title = "Enter sum, yo")
    print(f"You typed: {dialogue.get_input()}.")
    
def closeWindow(window):
    window.destroy()
    
def openTopLevel(master):
    window = ctk.CTkToplevel(master)
    window.geometry("500x500")
    label = ctk.CTkLabel(window,
                         text = "Label in a new window!",
                         font = ("Courier", 20))
    label.grid(row = 0,
               column = 0)
    closeButton = ctk.CTkButton(window,
                                text = "This closes the window!",
                                corner_radius = 20,
                                command = lambda: closeWindow(window))
    closeButton.grid(row = 1,
                     column = 0,
                     pady = 20,
                     padx = 20)

def main():
    
    root = ctk.CTk()
    root.geometry("1100x580")
    root.title("CTkinter Practice")
    
    frame1 = ctk.CTkFrame(root,
                          width = 1100,
                          height = 500)
    frame1.grid(row = 1,
                column = 0)
    
    titleLabel = ctk.CTkLabel(root, 
                         text = "Learning CTkinter and Grids",
                         font = ("Courier", 30))
    titleLabel.grid(row = 0,
                    column = 0,
                    ipady = 20,
                    ipadx = 10,
                    sticky = "w")
    
    progressBar = ctk.CTkProgressBar(frame1,
                                     determinate_speed=1/2,
                                     width = 1000)
    progressBar.grid(row = 0,
                     column = 0,
                     sticky = "w",
                     pady = 40)
    progressBar.set(0)
    
    startButton = ctk.CTkButton(frame1,
                                text = "Start",
                                font = ("Courier", 20),
                                command = lambda: startProgressBar(progressBar, startButton) )
    startButton.grid(row = 1,
                     column = 0,
                     sticky = "w",
                     pady = 20)
    
    midFrame = ctk.CTkFrame(frame1,
                            width = 1100)
    midFrame.grid(row = 2,
                  column = 0,
                  sticky = "w")
    
    holder = ctk.IntVar(value = 1)
    switch = ctk.CTkSwitch(midFrame, 
                           text = "This is a switch lol",
                           command = lambda: switcher(holder),
                           variable = holder,
                           onvalue = 1,
                           offvalue = 0)
    switch.grid(row = 0,
                column = 0,
                sticky = "w")
    
    slider = ctk.CTkSlider(midFrame,
                           from_ = 0, 
                           to = 100,
                           command = sliderFun)
    slider.grid(row = 1,
                column = 0,
                sticky = "w")
    
    dialogueButton = ctk.CTkButton(midFrame, 
                                   text = "Open Dialogue",
                                   command = dialogueFun)
    dialogueButton.grid(row = 0,
                        column = 1,
                        sticky = "w",
                        padx = 20)
    
    topLevelButton = ctk.CTkButton(midFrame, 
                                   text = "Open TopLevel",
                                   corner_radius = 30,
                                   command = lambda: openTopLevel(midFrame))
    topLevelButton.grid(row = 0,
                        column = 2,
                        sticky = "w",
                        padx = 20)
                       
    
    
    
    root.mainloop()
    


if __name__ == "__main__":
    main()