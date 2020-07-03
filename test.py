from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('test')
img = ImageTk.PhotoImage(Image.open('./Images/phone1.png'))
ibutt = Button(image=img)
ibutt.pack()


root.mainloop()