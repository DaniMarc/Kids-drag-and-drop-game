from tkinter import *
from PIL import ImageTk, Image
import random, os

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.w = 1200
        self.h = 700
        self.x_half = self.w/2
        self.y_half = self.h/2
        self.animal_type = None
        self.image_name = self.image_picker()
        self.image_id = None
        self.my_canvas = Canvas(root, width=self.w, height=self.h, bg="white")
        self.coord_label = Label(root)
        self.create_widgets()
        self.create_bindings()


    def create_widgets(self):
        global img
        #Canvas
        self.my_canvas.create_line(0, self.y_half, self.w, self.y_half, fill="black")
        self.my_canvas.create_line(self.x_half, self.y_half, self.x_half, self.h, fill="black")
        self.my_canvas.create_text(self.x_half/2, self.y_half-15, text="Animal salbatic", font=("Helvetica","20"), fill="red")
        self.my_canvas.create_text(self.x_half+self.x_half/2, self.y_half-15, text="Animal domestic", font=("Helvetica","20"), fill="green")
        self.my_canvas.create_rectangle(0, self.y_half, self.x_half, self.h, fill="#8a170f")
        self.my_canvas.create_rectangle(self.x_half, self.y_half, self.w, self.h, fill="#186b0c")
        #Image
        imgpath = self.image_name
        img = PhotoImage(file=imgpath)
        img = img.zoom(11)
        img = img.subsample(29)
        self.my_canvas.create_image(self.x_half, 125,image=img)
        # img = PhotoImage(file=self.image_name)
        # my_image = self.my_canvas.create_image(self.x_half, 125,image=img)

        self.my_canvas.pack(pady=20)
        #Coords Label
        self.coord_label.pack(pady=20)


    def create_bindings(self):
        self.my_canvas.bind('<B1-Motion>', self.move_image)


    # def starter_image(self):
    #     self.my_canvas.create_image(self.x_half, 125, image=self.image)


    def image_picker(self):
        global img
        an_type = random.randint(1,2)
        if an_type == 1:
            self.animal_type = "tamed/"
        else:
            self.animal_type = "wild/"

        dir = "../resources/animals/"
        dir = dir + self.animal_type
        
        pseudo_var = random.choice(os.listdir(dir))
        img = dir + pseudo_var
        return img


    def get_image(self):                                                                                
        global img, final_img
        img = Image.open(self.image_name)
        resize_img = img.resize((250,175), Image.ANTIALIAS)
        final_img = ImageTk.PhotoImage(resize_img)
        return final_img


    def move_image(self, event):
        img = self.get_image()
        self.image_id = self.my_canvas.create_image(event.x, event.y, image=img)
        self.coord_label.config(text="Cordonates: X=" + str(event.x) + " Y=" + str(event.y) + " image has ID: " +str(self.image_id))
    
        


#DRIVER CODE
root = Tk()
root.title('Drag and drop the animals')
root.iconbitmap("../resources/icon/paw_icon.ico")
root.geometry("1200x800")
app = Application(master=root)
app.mainloop()