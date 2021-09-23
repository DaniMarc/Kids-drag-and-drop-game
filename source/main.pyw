import pickle
from  tkinter import *
from pickle import *
from typing import Collection
from PIL import ImageTk, Image
import random, os
import copy
LARGE_FONT = ("helvetica", 20)
# ============================================================= BASE CLASS
class GamePilotClass(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.container = Frame(self)
        self.container.pack()

        Tk.wm_title(self, "Animalele lumii")
        Tk.iconbitmap(self, default="../resources/icon/paw_icon.ico")
        Tk.state(self, "zoomed")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, GameEngine, RankingsPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quit_game(self):
        Tk.destroy(self)


# ============================================================= START PAGE - MAIN MENU
class StartPage(Frame):
    def __init__(self, parent, controller):
        global play_btn, rank_btn, exit_btn, bg_img, title_img
        Frame.__init__(self, parent)

        bg_img = PhotoImage(file="../resources/icon/background.png")
        bg_img_label = Label(self, image=bg_img)
        bg_img_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        title_img = PhotoImage(file="../resources/icon/title_icon.png")
        label = Label(self, image=title_img)
        label.pack()

        play_btn = PhotoImage(file="../resources/icon/play_button_icon2.png")
        rank_btn = PhotoImage(file="../resources/icon/rankings_button_icon2.png")
        exit_btn = PhotoImage(file="../resources/icon/exit_button_icon2.png")
        button1 = Button(self, image=play_btn, 
                            command=lambda: controller.show_frame(GameEngine), borderwidth=0)
        button1.pack(pady=10)
        button2 = Button(self, image=rank_btn, 
                            command=lambda: controller.show_frame(RankingsPage), borderwidth=0)
        button2.pack(pady=10)
        button3  = Button(self, image=exit_btn,
                            command=lambda: controller.quit_game(), borderwidth=0)
        button3.pack(pady=5)

        my_name_label = Label(self, text="© Game Developed by Marc Daniel / Joc realizat de Marc Daniel © \n • Contact: contact.dev.marc.daniel@gmail.com")
        my_name_label.pack()


# ============================================================= GAME ENGINE
class GameEngine(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        global game_title_img
        game_title_img = PhotoImage(file="../resources/icon/game_title_icon.png")
        label = Label(self, image=game_title_img)
        label.pack(pady=10)
        self.controller = controller

        self.image_counter = 0
        self.w = 1200
        self.h = 700
        self.x_half = self.w/2
        self.y_half = self.h/2
        self.points = 0
        self.animals_detected = []
        self.animal_type = None
        self.animal_name = None
        self.name_id = None
        self.image_id = None
        self.points_id = None
        self.points_score_text_id = None
        self.image_name = self.image_picker()
        self.my_canvas = Canvas(self, width=self.w, height=self.h, bg="white")
        self.coord_label = Label(self)
        self.create_widgets()
        self.create_bindings()


    def create_widgets(self):
        global img, wild_icon, tamed_image
        #Canvas
        self.my_canvas.create_line(0, self.y_half, self.w, self.y_half, fill="black")
        self.my_canvas.create_line(self.x_half, self.y_half, self.x_half, self.h, fill="black")
        self.points_score_text_id = self.my_canvas.create_text(self.x_half/4, 50, text="Scor: ")
        self.points_id =  self.my_canvas.create_text(self.x_half/4+20, 50, text=str(self.points))
        self.name_id = self.my_canvas.create_text(self.x_half, 20, text=self.animal_name, font="Helvetica")
        #WILD ANIMALS
        self.my_canvas.create_text(self.x_half/2, self.y_half-15, text="Animal sălbatic", font=("Helvetica","20"), fill="red")
        self.my_canvas.create_rectangle(0, self.y_half, self.x_half, self.h, fill="#8a170f")
        wild_icon = PhotoImage(file="../resources/icon/wild_icon.png")
        self.my_canvas.create_image(self.x_half/2, self.y_half+self.y_half/2,image=wild_icon)
        #TAMED ANIMALS
        self.my_canvas.create_text(self.x_half+self.x_half/2, self.y_half-15, text="Animal domestic", font=("Helvetica","20"), fill="green")
        self.my_canvas.create_rectangle(self.x_half, self.y_half, self.w, self.h, fill="#186b0c")
        tamed_image = PhotoImage(file="../resources/icon/tamed_icon.png")
        self.my_canvas.create_image(self.x_half+self.x_half/2, self.y_half+self.y_half/2,image=tamed_image)
        #Image
        imgpath = self.image_name
        img = PhotoImage(file=imgpath)
        img = img.zoom(11)
        img = img.subsample(29)
        self.image_id = self.my_canvas.create_image(self.x_half, 125,image=img)
        #Pack the Canvas on the GUI
        self.my_canvas.pack(pady=15)
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


    def reinit_image(self):
        if len(self.animals_detected) == 9:
            self.game_over()
        self.image_name = self.image_picker()
        while self.animal_name in self.animals_detected:
            self.image_name = self.image_picker()
        else:
            self.animals_detected.append(self.animal_name)
            
        img = self.get_image()
        self.my_canvas.create_image(self.x_half, 125,image=img)
        self.my_canvas.itemconfig(self.name_id, text=self.animal_name)
        

    def reset_image(self):
        img = self.get_image()
        self.my_canvas.create_image(self.x_half, 125,image=img)
        self.my_canvas.itemconfig(self.name_id, text=self.animal_name)


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
                self.my_canvas.itemconfig(self.points_score_text_id, fill="green")    
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="green")
            else: 
                self.points -= 1
                self.reset_image()
                self.my_canvas.itemconfig(self.points_score_text_id, fill="red")
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="red")
        elif (event.y > self.y_half) and (event.x > self.x_half):
            if self.animal_type == "tamed/":
                self.points += 1
                self.reinit_image()
                self.my_canvas.itemconfig(self.points_score_text_id, fill="green")                
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="green")
            else: 
                self.points -= 1
                self.reset_image()
                self.my_canvas.itemconfig(self.points_score_text_id, fill="red")
                self.my_canvas.itemconfigure(self.points_id, text=str(self.points), fill="red")


    def submit_button_action(self):
        name = str(name_entry.get())
        if name != "":
            data_to_store = str(name + "," + str(self.points)+"\n")
            with open("rankdata", 'ab') as fp:
                pickle.dump(data_to_store,fp)
            fp.close()
            #Reset the game
            self.points = 0
            self.animals_detected.clear()
            pop.destroy()
            self.controller.show_frame(StartPage)
        else:
            fail_label = Label(my_frame, text="Nu ai scris numele!", bg="red")
            fail_label.pack()


    def game_over(self):
        global pop
        global name_entry 
        global my_frame
        pop = Toplevel(self)
        pop.title("Salvează-ți scorul!")
        pop.geometry("500x350")
        pop.config(bg="cyan")

        my_frame = Frame(pop, bg="cyan")
        my_frame.pack(pady=50)

        score_label = Label(my_frame, text="Felicitări! Scorul tău este: ")
        points_label = Label(my_frame, text=str(self.points), bg="green")
        pop_label = Label(my_frame, text="Introdu-ți numele:")

        name_entry = Entry(my_frame)
        submit_button = Button(my_frame, text="Trimite scorul", command=lambda:self.submit_button_action())
        
        score_label.pack(pady=5)
        points_label.pack(pady=5)
        pop_label.pack(pady=10)
        name_entry.pack()
        submit_button.pack(pady=15)
        



# ============================================================= RANKING SYSTEM
class RankingsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        label = Label(self, text="Clasament", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.w = 1200
        self.h = 700
        self.x_half = self.w/2
        self.y_half = self.h/2
        self.ranks_canvas = Canvas(self, width = self.w, height=self.h, bg="white")
        self.ranks_canvas.pack(pady=5)
        button1 = Button(self, text="Înapoi la meniul principal", 
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(side="right")
        button2 = Button(self, text="Reîmprospătează clasamentul", command=lambda: self.display_ranking())
        button2.pack(side="left")
        self.display_ranking()

    
    def __unpickle_data(self):
        p_data = []
        with open('rankdata', 'ab') as tf:
            pass
        tf.close()
        with open("rankdata", 'rb') as fr:
            try:
                while True:
                    p_data.append(pickle.load(fr))
            except EOFError:
                pass
        fr.close()
        return p_data


    def display_ranking(self):
        self.ranks_canvas.delete('all')
        raw_data = self.__unpickle_data()
        converted_data = {}
        for player in raw_data:
            player_name = player.split(',')[0]
            player_score = player.split(',')[1]
            converted_data[player_name] = int(player_score)
        sorted_data = dict(reversed(sorted(converted_data.items(), key=lambda item: item[1])))
        index = 1
        separation_index = 50
        for player in sorted_data.keys():
            display_string = str(str(index)+". "+player+" cu scorul: "+str(sorted_data[player]))
            self.ranks_canvas.create_text(self.x_half, separation_index, text=display_string, font=("Helvetica", "15"))
            index += 1
            separation_index += 50

#DRIVER CODE
app = GamePilotClass()
app.mainloop()