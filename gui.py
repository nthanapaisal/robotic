#interface
import tkinter as tk
from tkinter import font as tkfont

#QR
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from scanQR import runScanner

#tools
import time

class interQLADZ(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #rasp resolution
        self.geometry('800x480')
        #program text
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (HomePage,ScanPage,InfoPage,confirmPage,loadingPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")



    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome to Screen-Bozz",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        qrButton = tk.Button(self,text="Scan your QR code",
                            command=lambda: controller.show_frame("ScanPage"))
        
        payButton = tk.Button(self,text="Pay with cash")
        

        qrButton.pack()
        payButton.pack()
        

class ScanPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Please Scan your QR code",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        #bring in QR scanner + return user info
        #runScanner()














        skipButton = tk.Button(self,text="Skip",
                                command=lambda: controller.show_frame("InfoPage"))
        skipButton.pack()


        backButton = tk.Button(self,text="Go back",
                            command=lambda: controller.show_frame("HomePage"))
        backButton.pack()

class InfoPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Confirm your information",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        #show user data
        
        
        
        
        confirmButton = tk.Button(self,text="Confirm",
                                command=lambda: controller.show_frame("confirmPage"))
        confirmButton.pack()
        
        backButton = tk.Button(self,text="Go back",
                                command=lambda: controller.show_frame("ScanPage"))
        backButton.pack()


class confirmPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select your phone then start",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        #implement hardware when confirmButtom is clicked
        
        
        
        
        
        confirmButton = tk.Button(self,text="Start Screen Chaning",
                                command=lambda: controller.show_frame("loadingPage"))
        confirmButton.pack()
        
        backButton = tk.Button(self,text="Go back",
                                command=lambda: controller.show_frame("InfoPage"))
        backButton.pack()

class loadingPage(tk.Frame):
    def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            label = tk.Label(self, text="Processing",font=controller.title_font)
            label.pack(side="top", fill="x", pady=10)

            #if that many seconds return to main page...
            
        
        
        
        
if __name__ == "__main__":
    app = interQLADZ()
    app.mainloop()