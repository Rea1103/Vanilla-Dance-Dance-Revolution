from tkinter import *
from PIL import ImageTk, Image
import random
import RPi.GPIO as GPIO

# creating a class for the main window
class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) # inherits the class Tk()
        self.title('Game')
        self.geometry('800x800') # not dynamic enough to scale according to screen size

        # dimensions config
        self.width = 800
        self.height = 800

        # creation of Frame that will be as big as the window
        container = Frame(self, height=self.height, width=self.width)
        # specifying the region where the frame is packed in root
        container.pack(side='top', fill='both', expand='True')
        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1) # weight determines how wide the column will occupy relative to other columns
        container.grid_columnconfigure(0, weight=1)

        # creation of dictionary of frames
        self.frames = {}
        for F in (HomeScreen, GamePage, TutorialPage):
            frame = F(container, self)
            # the window class acts as the root window for the frames
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        # set first page as the default landing page
        self.show_frame(HomeScreen)

    
    # creating a method to switch view frames
    def show_frame(self, container):
        frame = self.frames[container]
        # raises the current frame to the top
        frame.tkraise()


    # closes the whole window - shuts down game
    def stop_game(self):
        self.quit()


# creating a class for the home screen page via Frame
class HomeScreen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent) # inherits the class Frame()

        title_label = Label(self, text='Welcome to our game :D', font=('Terminal', 16))
        title_label.pack(padx=20, pady=40)

        # using button to call show_frame() as a lambda function
        # play button directs player to GamePage Frame to continue playing
        play_button = Button(self, text='Play game', font=('Courier', 14), command=lambda:controller.show_frame(GamePage))
        play_button.pack(padx=20, pady=20)

        # tutorial button directs player to tutorials
        tutorial_button = Button(self, text='How to play?', font=('Courier', 14), command=lambda:controller.show_frame(TutorialPage))
        tutorial_button.pack(padx=20, pady=20)

        # quit button directs to stop_game() function under Window() class to shut down the game
        quit_button = Button(self, text='Quit game', font=('Courier', 14), command=lambda:controller.stop_game())
        quit_button.pack(padx=20, pady=20)


# creating a class for the game page via Frame
class GamePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # creating the canvas to put our arrows on + animate them
        self.canvas = Canvas(self, width=800, height=800, bg='white')
        self.canvas.pack()
        
        # creating a storage for player input to be kept in
        self.player_input = None # default to None
        # to keep track of player's movement
        self.player_correct = False

        # dimensions config
        self.width = 800
        self.height = 800
        self.mid_arrow = 120//2 # for now arrow sizes are 120 x 89

        # defining the scoring system
        self.correct = 0
        self.wrong = 0

        # creating a line at the background
        self.line = self.canvas.create_line(0,650,self.width,650, fill='black', width=4)

        # creating a label to show the number of lives the player has
        self.lives_message = 'Lives left: X X X'
        self.lives_label = Label(self, text=self.lives_message, font=('Courier', 12), bg='white')
        self.lives = self.canvas.create_window(10, 10, window=self.lives_label, anchor='nw')

        # creating a label to show the player's score
        self.score_message = 'Score: ' + str(self.correct)
        self.score_label = Label(self, text=self.score_message, font=('Courier', 12), bg='white')
        self.lives = self.canvas.create_window(700, 10, window=self.score_label, anchor='nw')

        # adding the file path of image arrows
        self.left_arrow_img = ImageTk.PhotoImage(Image.open(r"Assets/arrow-left.png"))
        self.right_arrow_img = ImageTk.PhotoImage(Image.open(r"Assets/arrow-right.png"))
        self.up_arrow_img = ImageTk.PhotoImage(Image.open(r"Assets/arrow-up.png"))
        self.down_arrow_img = ImageTk.PhotoImage(Image.open(r"Assets/arrow-down.png"))

        # creating a label to show the arrows
        self.arrow_label = Label(self, bg='white')
        self.chosen_arrow = None # placeholder for randomised arrow later on
        self.arrow_1 = self.canvas.create_window(self.width//2-self.mid_arrow+40, 10, window=self.arrow_label, anchor='nw')
        
        # create a button that directs player back to main page
        self.continue_button = Button(self, text='Continue', font=('Courier', 14), command=lambda:controller.show_frame(HomeScreen))

        # defining the starting message
        self.message = ['GO!', '1...', '2...', '3...'] # these messages will be pop() later on
        self.starting_label = Label(self, font=('Courier', 18), bg='white')
        self.starting_message = self.canvas.create_window(self.width//2-10, self.height//4, window=self.starting_label, anchor='nw')
	
	
    # overwriting the tkraise from the parent class Frame so that
    # whenever the frame is called, do the starting sequence
    def tkraise(self):
        super().tkraise() # inherits tkraise() from parent class Frame
        self.starting_screen() # adds on the self.starting_screen() sequence to start the game


    # function that listens to the player's input
    def listen_input(self):
		# if plate is pressed, it returns 1
        if GPIO.input(left_plate):
            self.player_input = 'Left'
        elif GPIO.input(right_plate):
            self.player_input = 'Right'
        elif GPIO.input(up_plate):
            self.player_input = 'Up'
        elif GPIO.input(down_plate):
            self.player_input = 'Down'

    
    # function that loads the pfop-up count down before the start of the game
    def starting_screen(self):
        if len(self.message) != 0:
            self.starting_label.config(text=self.message.pop())
            self.after(2000, self.starting_screen) # 1000 is too short
        else:
            # proceed to show the arrow after the player headsup is shown
            return self.show_arrow()


    # function that get's called upon losing 3 lives (game over)
    def game_over(self):
        # creating a label for 'game over' text
        self.game_over_label = Label(self, text='GAME OVER', font=('Courier', 18), bg='white')
        self.game_over_message = self.canvas.create_window(self.width//2-45, self.height//4, window=self.game_over_label, anchor='nw')
        
        # removes the arrows png
        self.arrow_label.destroy()
        
        # show the button that directs player back to main page
        self.continue_button.place(x=self.width//2-30, y=self.height//2)


    # function that randomises the order of arrows getting drops
    def get_arrow(self):
        number = random.randint(1,4)
        if number == 1:
            return (self.left_arrow_img, 'Left')
        elif number == 2:
            return (self.right_arrow_img, 'Right')
        elif number == 3:
            return (self.up_arrow_img, 'Up')
        else:
            return (self.down_arrow_img, 'Down')


    # function that gets called to (1) retrieve the next arrow, (2) set things to their default positions
    def change_arrow(self):
        # retrieve an arrow image and update the label for arrow
        self.chosen_arrow = self.get_arrow()
        self.arrow_label.config(image=self.chosen_arrow[0], bg='white')
        # default arrow to starting position
        self.canvas.coords(self.arrow_1, self.width//2-self.mid_arrow, 10)

        # default to black line
        self.canvas.itemconfig(self.line, fill='black') 

        # default back to False
        self.player_correct = False
        # player input defaults back to None
        self.player_input = None


    # function that gets called at the start of the game to (1) remove count down, (2) start the drop animation
    def show_arrow(self):
        # delete the count down message
        self.starting_label.destroy()

        # retrieve an arrow image and update the label for arrow
        self.change_arrow()

        # proceed to drop animation
        self.drop()


    # function that (1) animating the movement of the arrows, (2) checks for user input, 
    # (3) calculates score & lives remaining
    def drop(self):
        pos = self.canvas.coords(self.arrow_1) # returns [x, y]
        
        # case 1: player hits the correct button at the correct time/ y-coordinate of object
        if 610 <= pos[1] <= 620: # 10 frame interval
            # code only listens for input at this specified range
            # hence when a player tries to give an answer early, it will be invalidated
            self.listen_input()
            # print(self.player_input, self.chosen_arrow[1]) # for debugging

            # check if player input is correct
            if self.player_correct == False: # no correct input from player yet
                if self.player_input == self.chosen_arrow[1]:
                    self.player_correct = True

                    # notify the player that they are correct -> black line turns green
                    self.canvas.itemconfig(self.line, fill='green')

                    # add 1 to the 'correct' scoring system
                    self.correct += 10
                    # update the score system
                    self.score_message = 'Score: ' + str(self.correct)
                    self.score_label.config(text=self.score_message)

                    # player input defaults back to None
                    self.player_input = None

        if pos[1] == 640 and self.player_correct == True: 
            # must give 10/20 frame gap to allow the line to turn green
            # start bringing things to default position/ values
            self.change_arrow()


        # case 2: player misses the arrow
        elif pos[1] == 650:
            # notify the player that they miss the arrow -> black line turns red
            self.canvas.itemconfig(self.line, fill='red')

            # add 1 to the 'wrong' scoring system
            self.wrong += 1
            # remove one life from their life bank & update their life bank
            self.lives_message = self.lives_message[:-2]
            self.lives_label.config(text=self.lives_message)

            # check if the player made a mistake for more than 3 times
            if self.wrong == 3:
                return self.game_over()
                
        elif pos[1] == 670:
            # must give 20 frame gap to allow the line to turn red
            # start bringing things to default position/ values
            self.change_arrow()
            

        # dropping animation, move 10 pixels every 0.05 seconds
        self.canvas.move(self.arrow_1, 0, 5) # 70, 10

        self.after(40, self.drop) # recursive loop


# creating a class for the tutorial page via Frame
class TutorialPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent) # inherits the class Frame()

        # creating a label for the title
        title_label = Label(self, text='How to play:', font=('Terminal', 16))
        title_label.pack(padx=20, pady=20)

        # creating a label to show the instructions
        self.tutorial_message = '' # placeholder for tutorial instructions
        self.read_tutorial()
        tutorial_label = Label(self, text=self.tutorial_message, font=('Courier', 14))
        tutorial_label.pack(padx=20, pady=20)

        # tutorial button directs player to back to homescreen
        tutorial_button = Button(self, text='Back to home', font=('Courier', 14), command=lambda:controller.show_frame(HomeScreen))
        tutorial_button.pack(padx=20, pady=20)


    # reads the tutorial text file
    def read_tutorial(self):
        with open('Assets/tutorials.txt', 'r') as f:
            for line in f:
                self.tutorial_message += line


# setting up GPIO pins to bind the player's input
GPIO.setmode(GPIO.BOARD) # uses physical numbering system

# connect one each plate/button to 5V pin while the other end connects to their respective GPIO
# setting up GPIO pins to bind the player's input
GPIO.setmode(GPIO.BOARD) # uses physical numbering system

#arrow left will use GPIO 17, physical pin: 11
left_plate = 11
GPIO.setup(left_plate, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#arrow down will use GPIO 23, physical pin: 16
down_plate = 16
GPIO.setup(down_plate, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#arrow right will use GPIO 24, physical pin: 18
right_plate = 28
GPIO.setup(right_plate, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#arrow up will use GPIO 27, physical pin: 13
up_plate = 13
GPIO.setup(up_plate, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# main code
if __name__ == '__main__':
    window = Window()
    window.mainloop()
