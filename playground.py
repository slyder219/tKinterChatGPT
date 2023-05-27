import tkinter as tk
from tkinter import filedialog

def saveHistory(outputBox):
    # Getting all the history 
    outputBox.configure(state = "normal")
    histText = outputBox.get("0.0", "end")

    # Prompt user for file name
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])

    if filename:
        with open(filename, "w") as f:
            # write string to file
            f.write(histText)