import sys
import customtkinter as ctk
import openai 
import datetime
import os
import keyboard
from tkinter.filedialog import askopenfile
import ast
from tkinter import filedialog

sys.path.append(r"C:\Users\seanl\AppData\Local\Programs\Python\Python311\Lib\site-packages")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

key = os.environ.get("OPENAI_API_KEY")
openai.api_key = key

# Class we'll use to store the conversation and its abilities 
class convo():
    def __init__(self):
        self.temp = 0.6
        self.model = "gpt-3.5-turbo"
        # History fed to chatgpt everytime to allow an ongoing conversation. 
        self.history = []
        # Allows easy reference to display the response
        self.latestTextOut = ""

    # Routes the user's message to it 
    def message(self, newMessage):
        self.history.append(
            {"role": "user", "content": newMessage}
        )
        # Generate the chat completion / response
        response = openai.ChatCompletion.create(
            model = self.model,
            messages = self.history,
            temperature = self.temp
        )
        # Extract just the message 
        textOut = response.choices[0].message.content
        # Add its own response to the history so it knows what its already said 
        self.history.append(
            {"role": "assistant", "content": textOut}
        )
        self.latestTextOut = textOut
    # Little function to basically reset its memory 
    def newchat(self):
        self.history.clear()
    def updateOutputBox(self, outputBox):
        outputBox.configure(state = "normal")
        outputBox.delete("0.0", "end")
        for i in range(len(self.history)):
            outputBox.insert("end", self.history[i]["content"])
            if "user" in self.history[i]["role"]:
                outputBox.insert("end", "\n")
            if "assistant" in self.history[i]["role"]:
                outputBox.insert("end", "\n----------------------------------\n")
        outputBox.configure(state = "disabled")
# Triggered by a button in the past but now just tied to cntl + enter 
def enterPressed(inputBox, outputBox, convoClass):
    # Gets input
    textIn = inputBox.get("0.0", "end")

    # To essentially show used that the completion is loading, we take away their cursor and grey the input 
    inputBox.configure(text_color = "grey")
    inputBox.configure(state = "disabled")

    # Use that class to process the interaction
    convoClass.message(textIn)
    textOut = convoClass.latestTextOut

    # Make input look normal now to show done loading 
    inputBox.configure(state = "normal")
    inputBox.configure(text_color = "white")
    # Clear to prep for next input 
    inputBox.delete("0.0", "end")

    # Adding both user input and chatgpt's output to the big outputBox to mimick a chat 
    outputBox.configure(state = "normal")
    outputBox.insert("end", textIn)
    outputBox.insert("end", "\n")
    outputBox.insert("end", textOut)
    outputBox.insert("end", "\n")
    outputBox.insert("end", "----------------------------------\n")
    outputBox.see("end")
    outputBox.configure(state = "disabled")

# Temp is chatgpt's level of confidence in its answers. This program lets the user change it whenever
def changeTemp(tempEntry, convoClass):
    # Uses a textbox and button to communicate with the user how to get good input (0 - 1) 
    newTemp = tempEntry.get("0.0", "end")
    try:
        floatTemp = float(newTemp)
        if floatTemp <= 1 and floatTemp >= 0:
            convoClass.temp = floatTemp
            tempEntry.delete("0.0", "end")
            tempEntry.insert("0.0", "New temp set to: ")
            tempEntry.insert("end", convoClass.temp)
        else: 
            tempEntry.delete("0.0", "end")
            tempEntry.insert("0.0", "Value must be a number between 0 and 1")  
    except ValueError:
        tempEntry.delete("0.0", "end")
        tempEntry.insert("0.0", "Value must be a number between 0 and 1")

# Feature to save current chat history to your desktop named with the current date 
def saveHistory(outputBox):
    # Getting all the history 
    outputBox.configure(state = "normal")
    histText = outputBox.get("0.0", "end")

    # Get date and make file and write to file
    # now = datetime.datetime.now()
    # date_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    # desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    # filename = os.path.join(desktop_path, f"{date_str}.txt")

    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "w") as f:
            # write string to file
            f.write(histText)

    outputBox.configure(state = "disabled")

# Displays help info in its own textbox. I could premenantly display it but buttons are fun. 
def displayHelp(helpBox):
    # Get the text from the help txt file 
    with open(r"C:\Users\seanl\Documents\Personal\Coding\ChatGPT\tKinterChatGPT\help.txt", "r") as file:
        helpText = file.read()
    
    # Put it in the textbox 
    helpBox.configure(state = "normal")
    helpBox.insert("0.0", helpText)
    helpBox.configure(state = "disabled")

# Newchat function that a button will call which then calls the class' new chat function
def newChat(outputBox, convoClass):
    # Clear history 
    outputBox.configure(state = "normal")
    outputBox.delete("0.0", "end")
    outputBox.configure(state = "normal")

    convoClass.newchat()

def openHistoryFromFile(convoClass, outputBox):
    file = askopenfile(mode ='r', filetypes =[('Python Files', '*.txt')])
    if file is not None:
        filepath = file.name
        with open(filepath, "r") as f:
            content = f.read()
            new = ast.literal_eval(content)
            convoClass.history = new 
    convoClass.updateOutputBox(outputBox)

def saveMessageList(convoClass):
    toSave = str(convoClass.history)

    # now = datetime.datetime.now()
    # date_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    # desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    # filename = os.path.join(desktop_path, f"Advanced_{date_str}.txt")
    
    filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if filename:
        with open(filename, "w") as f:
            # write string to file
            f.write(toSave)    

def main():
    # Start the convo object 
    currentConvo = convo()

    # Set up tkinter window 
    root = ctk.CTk()
    root.geometry("1000x700")
    root.title("My ChatGPT lol")

    # Using a two-tab tabview to handle the chat interace and also the settings interface 
    tabs = ctk.CTkTabview(root,
                          width = 1000,
                          height = 700)
    tabs.grid(row = 0, column = 0)

    # add those two tabs 
    chat = tabs.add("Chat")
    settings = tabs.add("Settings")

    # In the chat tab, creating output and input textboxes
    outputBox = ctk.CTkTextbox(chat,
                               height = 400,
                               width = 900,
                               wrap = "word")
    outputBox.grid(row = 0,
                   column = 0,
                   columnspan = 6,
                   padx = 50,
                   pady = 10)
    outputBox.configure(state = "disabled")
    
    inputBox = ctk.CTkTextbox(chat, 
                              width = 900,
                              height = 150,
                              wrap = "word") 
    inputBox.grid(row = 1,
                  rowspan = 2,
                  column = 0,
                  columnspan = 3,
                  padx = 50,
                  pady = 10)
    
    # Not using an enter button so letting user know how to send 
    caption = ctk.CTkLabel(chat, 
                           text = "Send with cntrl + enter.",
                           font = ("Times New Roman", 15))
    caption.grid(row = 3,
                 column = 2,
                 columnspan = 3)

    # Now on the settings tab, adding textbox and button to handle temp change 
    tempEntry = ctk.CTkTextbox(settings,
                             width = 700,
                             height = 50,
                             wrap = "word")
    tempEntry.grid(row = 0,
                   column = 0,
                   columnspan = 6,
                   padx = 150,
                   pady = 5)
    tempEntry.insert("0.0", "Enter temp here. 0 - 1.")

    tempButton = ctk.CTkButton(settings,
                            width = 700,
                            height = 50,
                            text = "Change Temperature",
                            command = lambda: changeTemp(tempEntry, currentConvo))
    tempButton.grid(row = 1,
                 column = 0,
                 columnspan = 6,
                 padx = 150,
                 pady = 5)
     
    frameSpacer = ctk.CTkFrame(settings,
                               width = 700,
                               height = 50,
                               fg_color = "transparent") 
    frameSpacer.grid(row = 2,
                     column = 0,
                     columnspan = 6,
                     padx = 150,
                     pady = 5)
    
    # New chat button tied to above new chat functions 
    newChatButton = ctk.CTkButton(frameSpacer,
                                  width = 700,
                                  height = 50,
                                  text = "Clear Chat / New Chat",
                                  command = lambda: newChat(outputBox, currentConvo))
    newChatButton.grid(row = 0,
                       column = 0, 
                       padx = 0,
                       pady = 0)
    
    # Save history button tied to above save history funciton
    saveButton = ctk.CTkButton(settings,
                               width = 700,
                               height = 50,
                               text = "Save Current Conversation",
                               command = lambda: saveHistory(outputBox))
    saveButton.grid(row = 3, 
                    column = 0,
                    columnspan = 6,
                    pady = 5)
    
    frameSpacer2 = ctk.CTkFrame(settings, 
                                width = 700,
                                height = 50,
                                fg_color = "transparent")
    frameSpacer2.grid(row = 4,
                      column = 0,
                      columnspan = 6,
                      padx = 150,
                      pady = 5)
    
    advancedSaveButton = ctk.CTkButton(frameSpacer2,
                                       width = 700,
                                       height = 50,
                                       text = "ADVANCED: Save Message List",
                                       command = lambda: saveMessageList(currentConvo))
    advancedSaveButton.grid(row = 0,
                            column = 0)
    
    uploadHistoryButton = ctk.CTkButton(settings,
                                        width = 700,
                                        height = 50,
                                        text = "ADVANCED: Upload Message List",
                                        command = lambda: openHistoryFromFile(currentConvo, outputBox)
                                        )
    uploadHistoryButton.grid(row = 5,
                             column = 0,
                             columnspan = 6,
                             pady = 5)

    # Will display all that help text from the file. Help Text Box is transparent so the button kind
    #   just makes the help info appear which is kinda fun 
    helpButton = ctk.CTkButton(settings, 
                               width = 700,
                               height = 50,
                               text = "Help",
                               command = lambda: displayHelp(helpBox) )
    helpButton.grid(row = 6,
                    column = 0,
                    columnspan = 6,
                    pady = 5)
                    

    helpBox = ctk.CTkTextbox(settings, 
                             width = 700,
                             height = 200,
                             wrap = "word",
                             fg_color="transparent")
    helpBox.grid(row = 7,
                 column = 0, 
                 columnspan = 6)
    helpBox.configure(state = "disabled")



    # Adding that cntrl + enter to send message. Not binding to input box because I want it to 
    #   do this no matter what. 
    keyboard.add_hotkey('ctrl+enter', lambda: enterPressed(inputBox, outputBox, currentConvo) )

    

    # mainloop for tkinter 
    root.mainloop()

if __name__ == "__main__":
    main()
