from tkinter import *
from PIL import ImageTk, Image

#Starting main things
root = Tk()
root.title('Drag and drop the animals')
root.iconbitmap("../resources/icon/paw_icon.ico")
root.geometry("1200x800")

#Define the window logistics
w = 1200 #width
h = 700 #height
x_half = w/2
y_half = h/2

######################################################################## Prepare the working space
#Prepare the Canvas
my_canvas = Canvas(root, width=w, height=h, bg="white")
my_canvas.create_line(0, y_half, w, y_half, fill="black")
my_canvas.create_line(x_half, y_half, x_half, h, fill="black")
my_canvas.create_text(x_half/2, y_half-15, text="Animal salbatic", font=("Helvetica","20"), fill="red")
my_canvas.create_text(x_half+x_half/2, y_half-15, text="Animal domestic", font=("Helvetica","20"), fill="green")
my_canvas.create_rectangle(0, y_half, x_half, h, fill="#8a170f")
my_canvas.create_rectangle(x_half, y_half, w, h, fill="#186b0c")
my_canvas.pack(pady=20)

#Get the image for the beginning and places is in the center
img = Image.open("../resources/animals/wild/bear.png")                  #!! <+++++++++++++++++++_
resize_img = img.resize((250,175), Image.ANTIALIAS)                                             #\
final_img = ImageTk.PhotoImage(resize_img)                                                       #|
my_canvas.create_image(x_half/1.25, 45, anchor=NW, image=final_img)                              #|
                                                                                                 #|
                                                                                                 #|
######################################################################### Moving the image       #|
#Function that extracts the image from the resources                                             #|
def get_image():                                                                                 #|
    global img, final_img                                                                        #|
    img = Image.open("../resources/animals/wild/bear.png") #!!! works only bcs it's the same image|
    resize_img = img.resize((250,175), Image.ANTIALIAS)
    final_img = ImageTk.PhotoImage(resize_img)
    return final_img


#The motor function for the dragging mechanism
def move_image(event):
    img = get_image()
    my_canvas.create_image(event.x, event.y, image=img)
    my_label.config(text="Cordonates: X=" + str(event.x) + " Y=" + str(event.y))

#Label used in the 'move_image' function to display cordonates (debug reasons)
my_label = Label(root)
my_label.pack(pady=20)






root.mainloop()