import tkinter as tk
from tkinter import ttk, Label
from PIL import ImageTk, Image
from tkinter import filedialog
from functools import partial
import random
from time import sleep
import os
import functools
import threading

from kraken_images import transcribe


class Page1(tk.Frame):
	
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.timer_value = 300
        self.controller = controller
        self.num = -1
        self.ln = -1

        num_pth = "..\\ocr-post-correction\\dataset\\images_lines_kraken\\info.txt" 
        if os.path.isfile(num_pth):
            f = open(num_pth, "r")
            self.num = int(f.readline())
            self.ln = int(f.readline())
        

        pth = "..\\ocr-post-correction\\dataset\\images_lines_kraken\\"
        if (self.num == -1): self.num = 1;
        if (self.ln == -1): self.ln = len([entry for entry in os.listdir(pth) if os.path.isfile(os.path.join(pth, entry))])


        frame1 = tk.Frame(master=self, width=200, height=100) #, bg="red")
        frame1.pack(fill=tk.BOTH, side=tk.TOP, expand=False)

        frame2 = tk.Frame(master=self, width=100) #, bg="yellow")
        frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        frame3 = tk.Frame(master=self, width=50) #, bg="blue")
        frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        img = "..\\ocr-post-correction\\dataset\\images_lines_kraken\\auc_aco000136_000024_d7_correction.jpg"
        image = Image.open(img)

        basewidth = 500
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth,hsize), Image.Resampling.LANCZOS)

        photo = ImageTk.PhotoImage(image)
        self.label1 = Label(image=photo, master=frame1)


        self.greeting = tk.Label(master=frame1, text="Welcome")
        self.txt = "%s/%s" % (self.num, self.ln)
        self.greeting = tk.Label(master=frame1, text=self.txt)



        label = tk.Label(master=frame2, text="Correction")
        self.entry = tk.Entry(master=frame2, width=50)

        self.button = tk.Button(
            master=frame3,
            text="next",
            width=10,
            height=1,
            command=partial(self.store_input, self.label1)
        )

        timer_value = 300

        # Create a Label widget to display the timer
        self.timer_label = Label(master=frame1, text=str("00:00"))

        # label1 = tk.Label(master=frame1, text="I'm at (0, 0)", bg="red")
        # label1.place(x=0, y=0)
        self.greeting.pack()
        self.timer_label.pack(pady=20)
        self.label1.pack()
        label.pack()

        # Call the update_timer function to start the countdown
        self.update_timer()

        # label.pack()
        self.entry.pack()
        self.button.pack()
        # file_button.pack()
        # Function to update the timer
    
    def update_timer(self):

        # Calculate minutes and seconds
        minutes = self.timer_value // 60
        seconds = self.timer_value % 60

        # Format the timer value as a string in MM:SS format
        timer_text = f"{minutes:02d}:{seconds:02d}"

        # Update the timer label
        self.timer_label.configure(text=timer_text)

        # Check if the timer has reached 0
        if self.timer_value > 0:
            # Decrement the timer value
            self.timer_value -= 1
            # Schedule the next update after 1 second (1000 milliseconds)
            self.after(1000, self.update_timer)



    def store_input(self, lb):
        input_text = self.entry.get()
        print("Input stored:", input_text)

        


        
        pth = "..\\ocr-post-correction\\dataset\\images_lines_kraken\\auc_aco000136_000024_d%s_correction.jpg" % self.num
        new_image = Image.open(pth)
        # Create a Tkinter-compatible image
        
        basewidth = 500
        wpercent = (basewidth/float(new_image.size[0]))
        hsize = int((float(new_image.size[1])*float(wpercent)))
        new_image = new_image.resize((basewidth,hsize), Image.Resampling.LANCZOS)

        new_tk_image = ImageTk.PhotoImage(new_image)
        # Update the label with the new image
        lb.configure(image=new_tk_image)
        # Keep a reference to avoid garbage collection
        lb.image = new_tk_image
        # Add your desired functionality here
        self.num += 1
        
        nums = self.txt.split('/')
        nums[0] = str(self.num)
        self.txt = nums[0]+'/'+nums[1]

        self.greeting.configure(text=self.txt)

        self.ln=10
        if (self.num == self.ln): 
            self.button.configure(text="Finish")
            # transcribe.update_dataset()
            window = tk.Toplevel(self)
            txt = tk.Label(window, text="Do you want to start training").pack()
            button1 = tk.Button(
                master=window,
                text="yes",
                width=10,
                height=1,
                command=lambda : self.train_win(window)
            ).pack()

            button2 = tk.Button(
                master=window,
                text="no",
                width=10,
                height=1,
                command = lambda : self.close_win(window)
            ).pack()
        
    def close_win(self, win):
        self.controller.show_frame(StartPage)
        win.destroy()


    def train_win(self, win):
        self.controller.show_frame(StartPage)
        win.destroy()

        top = tk.Toplevel(self)  
        txt = tk.Label(top, text="Please wait for training to fininsh").pack()
             


   



# first window frame startpage

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text ="Startpage", font = LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        button1 = ttk.Button(self, text ="Continue on Current Book",
        command = lambda : controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)

        ## button to show frame 2 with text layout2
        # button2 = ttk.Button(self, text ="Page 2",
        # command = lambda : controller.show_frame(Page2))

        # # putting the button in its place by
        # # using grid
        # button2.grid(row = 2, column = 1, padx = 10, pady = 10)

        ## button to add book
        button3 = ttk.Button(self, text ="Add Book",
        command = self.get_dir)

        # putting the button in its place by
        # using grid
        button3.grid(row = 3, column = 1, padx = 10, pady = 10)
            
    def get_dir(self):
        # window.withdraw()
        folder_selected = filedialog.askdirectory()
        folder_selected += "\\"


        # transcribe.processBook(folder_selected)
                
        window = tk.Toplevel(self)
        tk.Label(window, text="OCR in progress...").pack()


        window.after(100, lambda: self.processDestroy(folder_selected, window))  # start the task after 100 ms

    def processDestroy(self, pth, top):
        # transcribe.processBook(pth)
        top.destroy()


LARGEFONT =("Verdana", 35)

class tkinterApp(tk.Tk):
	
	# __init__ function for class tkinterApp
	def __init__(self, *args, **kwargs):
		
		# __init__ function for class Tk
		tk.Tk.__init__(self, *args, **kwargs)
		
		# creating a container
		container = tk.Frame(self)
		container.pack(side = "top", fill = "both", expand = True)

		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		# initializing frames to an empty array
		self.frames = {}

		# iterating through a tuple consisting
		# of the different page layouts
		# for F in (StartPage, Page1, Page2):
		for F in (StartPage, Page1):

			frame = F(container, self)

			# initializing frame of that object from
			# startpage, page1, page2 respectively with
			# for loop
			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky ="nsew")

		# self.show_frame(StartPage)
		self.show_frame(StartPage)

	# to display the current frame passed as
	# parameter
	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

if __name__ == "__main__":
    # Driver Code
    app = tkinterApp()
    app.mainloop()
