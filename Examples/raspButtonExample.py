#!/usr/bin/env python3

import tkinter as tk
import tkinter.font as tkFont
import RPi.GPIO as GPIO

def ledON():
    print("LED button pressed")
    if GPIO.input(40):
        GPIO.output(40,GPIO.LOW)
        ledButton["text"] = "LED ON"
    else:
        GPIO.output(40,GPIO.HIGH)
        ledButton["text"] = "LED OFF"

def exitProgram():
    print("Exit Button pressed")
    GPIO.cleanup()
    win.quit()  

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.LOW)

win = tk.Tk()

myFont = tkFont.Font(family = 'Helvetica', size = 36, weight = 'bold')

win.title("First GUI")
win.geometry('240x480')

exitButton = tk.Button(win, text = "Exit"
                        , font = myFont
                        , command = exitProgram
                        , height =2 
                        , width = 6) 
exitButton.pack(side = tk.BOTTOM)

ledButton = tk.Button(win, text = "LED ON"
                        , font = myFont
                        , command = ledON
                        , height = 2
                        , width =8 )
ledButton.pack()

win.mainloop()
