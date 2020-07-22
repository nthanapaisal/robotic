#interface
import tkinter as tk
from tkinter import font as tkfont
from PIL import ImageTk,Image

#qrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode

#import RPi.GPIO as GPIO
class custQLADZ:

    
    def __init__(self):
        self.first = 'NaN'
        self.last = 'NaN'
        self.email = 'NaN'
        self.userID = 'NaN'
        self.exists = False



class webcam:
    def __init__(self,src=0):
        self.cam = cv2.VideoCapture(src)
        if not self.cam.isOpened():
            print("Unable to open the camera")
        self.cam.set(3,640)
        self.cam.set(4,480)
          
        
    def start(self):
    
        while self.stop:
                
            #reading using cam if not QR it is empty list
            success,img = self.cam.read()
            
            #decode scanned img and it has QR
            for barcode in decode(img):
                #get the userID from barcode var
                userID = barcode.data.decode('utf-8')
                
                #check if this userID exists in data base
                currCust.ID =  'Suptha'
                
                if userID == currCust.ID:
                    print('Scanning success')
                    self.stop = False
                    currCust.exists = True
                    break        
                    
            cv2.imshow('Result',img)
            cv2.waitKey(1)
            
    def stopF(self):
        self.stop = False
        self.cam.release()
        cv2.destroyAllWindows()
        


class interQLADZ(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        #rasp resolution
        self.geometry('800x480')
        #program text
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        #self.vidSrc = webcam()
        
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
        global cam
        flag = 1 
        
        if page_name == 'loadingPage':
            self.after(10000, self.show_frame, 'HomePage')
  
            #hardware turn on LED
            #GPIO.output(40,GPIO.HIGH)
            
        if page_name == 'HomePage':
           
           #GPIO.output(40,GPIO.LOW)
            
            currCust.exists = False
            #came back from scan page, turn off camera
            if cam.isOpened():
                cam.stopF()
            
        if page_name == 'ScanPage':
            cam.stop = True
            
            cam.start()
            #turn off camera when getting user data
            if currCust.exists:
                cam.stopF()
                self.after(0, self.show_frame, 'InfoPage')

                
                
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
        camArea = tk.Canvas(self,width = 640,height = 480)
        camArea.pack()
        #camArea.create_image(0, 0, image = cam, anchor =NW)

        skipButton = tk.Button(self,text="Skip",
                                command=lambda: controller.show_frame("InfoPage"))
        skipButton.pack()


        backButton = tk.Button(self,text="Go back",
                            command=lambda: controller.show_frame("HomePage"))
        backButton.pack()
        print('scan')
        

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
        print('info')

class confirmPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select your phone then start",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        
        #implement hardware when confirmButtom is clicked (required self because of garbage collection)
        self.phone1 = ImageTk.PhotoImage(Image.open('./images/phone1.png'))
        self.phoneClick1 = ImageTk.PhotoImage(Image.open('./images/phone1-2.png'))
        self.phone2 = ImageTk.PhotoImage(Image.open('./images/phone2.png'))
        self.phoneClick2 = ImageTk.PhotoImage(Image.open('./images/phone2-2.png'))
        self.phoneButt1 = tk.Button(self,image=self.phone1,command=lambda *args: self.setSize(1))
        self.phoneButt2 = tk.Button(self,image=self.phone2,command=lambda *args: self.setSize(2))
        self.phoneButt1.pack()
        self.phoneButt2.pack()
        
        confirmButton = tk.Button(self,text="Start Screen Chaning",
                                command=lambda: [controller.show_frame("loadingPage"),self.resetButtons()])
        confirmButton.pack()
        
        backButton = tk.Button(self,text="Go back",
                                command=lambda: [controller.show_frame("InfoPage"),self.resetButtons()])
                                                     
        backButton.pack()
        print('confirm')
        
    def setSize(self,size):
        global phoneSize
        #make sure the other one is not display as selected
        self.resetButtons()
        
        if size == 1:
            phoneSize = 10
            self.phoneButt1["image"] = self.phoneClick1
            
        elif size == 2:
            phoneSize = 12
            self.phoneButt2["image"] = self.phoneClick2
    
    def resetButtons(self):
        self.phoneButt1["image"] = self.phone1
        self.phoneButt2["image"] = self.phone2
        
class loadingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Processing",font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

    #update database -1 quantity, date/time stamp
        
#global values
phoneSize = 0
cam = webcam()
currCust = custQLADZ()
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(40, GPIO.OUT)
#GPIO.output(40, GPIO.LOW)

  
if __name__ == "__main__":
    app = interQLADZ()
    app.mainloop()