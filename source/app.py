from tkinter import *
from PIL import ImageTk, Image
import random, os
import copy

class GameEngine(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.image_counter = 0
        self.w = 1200
        self.h = 700
        self.x_half = self.w/2
        self.y_half = self.h/2
        self.points = 0
        self.animal_type = None
        self.animal_name = None
        self.name_id = None
        self.image_id = None
        self.points_id = None
        self.points_score_id = None
        self.image_name = self.image_picker()
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
        self.points_score_id = self.my_canvas.create_text(self.x_half/4, 50, text="Scor: ")
        self.points_id =  self.my_canvas.create_text(self.x_half/4+20, 50, text=str(self.points))
        self.name_id = self.my_canvas.create_text(self.x_half, 20, text=self.animal_name, font="Helvetica")
        self.my_canvas.create_rectangle(0, self.y_half, self.x_half, self.h, fill="#8a170f")
        self.my_canvas.create_rectangle(self.x_half, self.y_half, self.w, self.h, fill="#186b0c")
        #Image
        imgpath = self.image_name
        img = PhotoImage(file=imgpath)
        img = img.zoom(11)
        img = img.subsample(29)
        self.image_id = self.my_canvas.create_image(self.x_half, 125,image=img)
        #Pack the Canvas on the GUI
        self.my_canvas.pack(pady=20)
        #Coords Label
        self.coord_label.pack(pady=20)


    def create_bindings(self):
        self.my_canvas.bind('<B1-Motion>', self.move_image)
        self.my_canvas.bind('<ButtonRelease-1>', self.release_click)


    def image_picker(self):
        global img
        # 'Randomize' the animal kind
        an_type = random.randint(1,2)
        if an_type == 1:
            self.animal_type = "tamed/"
        else:
            self.animal_type = "wild/"
        #Creating the traj(dir)ectory with the pseudo-randomized animal type
        dir = "../resources/animals/"
        dir = dir + self.animal_type
        #Random pick the animal
        pseudo_var = random.choice(os.listdir(dir))
        self.animal_name = copy.deepcopy(pseudo_var)
        #Save only the name
        self.animal_name = self.animal_name[:-4]
        #Creating the path
        img = dir + pseudo_var
        return img #Saving the path to the image


    def get_image(self):                                                                                
        global img, final_img
        img = Image.open(self.image_name)
        resize_img = img.resize((250,175), Image.ANTIALIAS)
        final_img = ImageTk.PhotoImage(resize_img)
        return final_img


    def move_image(self, event):
        img = self.get_image()
        self.image_id = self.my_canvas.create_image(event.x, event.y, image=img)
        # self.coord_label.config(text="Cordonates: X=" + str(event.x) + " Y=" + str(event.y) + " image has ID: " +str(self.image_id))


    def release_click(self, event):
        if (event.y > self.y_half) and (event.x < self.x_half):
            if self.animal_type == "wild/":
                self.points += 1
                self.reinit_image()
                self.my_canvas.itemconfig(self.points_score_id, fill="green")    
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="green")
            else: 
                self.points -= 1
                self.reset_image()
                self.my_canvas.itemconfig(self.points_score_id, fill="red")
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="red")
        elif (event.y > self.y_half) and (event.x > self.x_half):
            if self.animal_type == "tamed/":
                self.points += 1
                self.reinit_image()
                self.my_canvas.itemconfig(self.points_score_id, fill="green")                
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="green")
            else: 
                self.points -= 1
                self.reset_image()
                self.my_canvas.itemconfig(self.points_score_id, fill="red")
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="red")


    def reinit_image(self):
        self.image_name = self.image_picker()
        img = self.get_image()
        self.my_canvas.create_image(self.x_half, 125,image=img)
        self.my_canvas.itemconfig(self.name_id, text=self.animal_name)
        

    def reset_image(self):
        img = self.get_image()
        self.my_canvas.create_image(self.x_half, 125,image=img)
        self.my_canvas.itemconfig(self.name_id, text=self.animal_name)
    
        


#DRIVER CODE
root = Tk()
root.title('Drag and drop the animals')
root.iconbitmap("../resources/icon/paw_icon.ico")
root.geometry("1200x800")
app = GameEngine(master=root)
app.mainloop()