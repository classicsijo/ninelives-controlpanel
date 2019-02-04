import tkinter as tk
from PIL import ImageTk, Image
import time
from pprint import pprint			#For variable dumping only
#import RPi.GPIO as GPIO			#Comment out for testing on Windows
#from pygame import mixer			#library for playing MP3

gameflowDict = {	"Start":"Game Started",
					"Cigar":"Cigar in Ashtray",
					"Whisky":"Whisky in Glass",
					"Enigma":"Enigma Code Pressed",
					"BombStart":"Bombing Raid Begins",
					"BombEnd":"Bombing Raid Ended",
					"Morse":"Morse Code Entered",
					"End":"Game Complete!"  }
					
Pin = { 			None: 1, None: 2,
					None: 3, None: 4,
					"Remote 1 OFF": 5, None: 6,
					"Remote 2 OFF": 7, 'Morse IN': 8,
					"Cigar OUT": 9, 'Buzzer IN': 10,
					"Cigar IN": 11, None: 12,
					"Whisky OUT": 13,
					"Whisky IN": 15, None: 16,
					None: 17, None: 18,
					"Enigma IN": 19, None: 20,
					"Engima FALSE": 16,
					"Enigma OUT": 18		}

def setup():
    global buzz
    global skip
    
	#GPIO.setmode(GPIO.BOARD)       		# Numbers GPIOs by physical location
	#GPIO.setup(buzzerPin, GPIO.OUT)   	# Set buzzerPin's mode is output
	#GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set Pin[Morse IN] mode to input, and pull up to high level(3.3V)
	#buzz = GPIO.PWM(buzzerPin, 1)			#Create frequency pulse to sound buzzer
	#buzz.ChangeFrequency(700)				#output Buzzer PWM
	
    skip = False

class gameFlow:
    def __init__(self, left_canvas): 
        for key,label in gameflowDict.items():
            gameflowDict[key] = gameElement(left_canvas, label)
            if key != "End":
                downArrow(left_canvas)

class game:
    def cigar():
        global skip
        #if skip == True or GPIO.input(Pin['Cigar IN']) == GPIO.HIGH:		#Comment out for testing on Windows
        if skip == True or (Pin['Cigar IN']) == 32:
            gameElement.complete(gameflowDict["Cigar"])
            statusUpdate['text'] = "Waiting for Whisky in Glass"
            skip = False
        else:
            root.after(1000, game.cigar)
            
    def whisky():
        global skip
        #if skip == True or GPIO.input(Pin[Whisky]) == GPIO.HIGH:			#Comment out for testing on Windows
        if skip == True or (Pin['Whisky IN']) == 32:						#Comment out for Pi
            gameElement.complete(gameflowDict["Whisky"])
            statusUpdate['text'] = "Waiting for Code in Enigma Machine"
            skip = False
        else:
            root.after(1000, game.whisky)
            
    def enigma():
        global skip
        #if skip == True or GPIO.input(Pin[Whisky]) == GPIO.HIGH:			#Comment out for testing on Windows
        if skip == True or Pin['Enigma IN'] == 32:							#Comment out for Pi
            gameElement.complete(gameflowDict["Enigma"])
            statusUpdate['text'] = "Beginning Bombing Raid"
            skip = False
        else:
            root.after(1000, game.enigma)
    
    def bombing():
        pass
        #statusUpdate['text'] = "Playing bombing.mp3"
        #gameElement.complete(gameflowDict["BombStart"])
        #remotePin1 = Pin['Remote 1 OFF']
        #root.after(9000, lambda remotePin1: remotePin1,"GPIO.HIGH")		      #Comment out for testing on Windows
        #statusUpdate['text'] = "Light 1 Off"
        #gameElement.complete(gameflowDict["BombEnd"])
    
    def morse():
        pass
        #statusUpdate['text'] = "Waiting for Morse Code Entry"
        #morseCode()		#Listen for correct morse code
        #gameElement.complete(gameflowDict["Morse"])
        #statusUpdate['text'] = "Morse Code Entered Correctly"
    
    def end():
        pass
        #gameElement.complete(gameflowDict["End"])
        #statusUpdate['text'] = "Game Finished"
        
    def run():
        game.cigar()
        game.whisky()
        game.enigma()
        #game.bombing()
        game.morse()
        game.end()
        
class gameElement:
	def __init__(self, left_canvas, textLabel):
		self.element = tk.Label(left_canvas, text=textLabel, bg="beige", width=30, pady=5, font=("Tahoma", 10, "bold"))
		pady = ((18,0),(0,0))[textLabel != "Game Started"]
		self.element.pack(padx = 15, pady=pady)
	
	def complete(label):
		label.element['bg'] = 'gold'

class downArrow:
    def __init__(self, left_canvas):
        self.down_arrow = ImageTk.PhotoImage(Image.open("down2.png"))
        self.arrow = tk.Label(left_canvas, image = self.down_arrow, bg="darkseagreen")
        self.arrow.image = self.down_arrow
        self.arrow.pack(pady=4)
        

class controlButtons:
    def __init__(self, right_canvas):
        self.unlock = tk.Button(right_canvas, text="unlock", bg="gray", width=18, command = self.lockTools)
        self.unlock.pack(pady=(282,0), padx=25)
        
        self.skip = tk.Button(right_canvas, text="Skip puzzle", bg="lightgray", width=18, state='disabled', command = self.puzzleSkip)
        self.skip.pack(pady=(20,0), padx=25)
        
        self.stop = tk.Button(right_canvas, text="Emergency Stop", bg="lightgray", width=18, state='disabled', command = self.emergencyStop)
        self.stop.pack(pady=(15,0), padx=25)
        
        self.start = tk.Button(right_canvas, text="Start Game", bg="lightgray", width=18, height=3, state='disabled', command = self.startGame)
        self.start.pack(pady=(40,0), padx=25)
    
    def lockTools(self):
        if self.unlock['text'] == "unlock":
            self.skip['state'] = self.stop['state'] = self.start['state'] = "normal"
            self.skip['bg'] = self.stop['bg'] = self.start['bg'] = "lightgreen"
            self.unlock['text'] = "lock"
            locked = False
        else:
            self.skip['state'] = self.stop['state'] = self.start['state'] = "disabled"
            self.skip['bg'] = self.stop['bg'] = self.start['bg'] = "lightgray"
            self.unlock['text'] = "unlock"
            locked = True
     
    def puzzleSkip(self):
        self.lockTools()
        global skip
        skip = True
    
    def emergencyStop(self):
        self.lockTools()
    
    def startGame(self):
        self.lockTools()
        gameElement.complete(gameflowDict["Start"])
        statusUpdate['text'] = "Waiting for Cigar in Ashtray"
        game.run()

class morseCode:
    def __init__(self):
        #buzz.start(0)		#Buzzer off at start
        buzzer_on = False
        buffer = ""
	
        # while True:
            # #if GPIO.input(Pin['Morse IN')==GPIO.LOW:					#Comment out for Windows testing
            # if True:													#Comment out for Pi Usage
                # self.alertor()
                # if buzzer_on==False:
                    # pressed = time.time()
                    # buzzer_on = True
            # else:
                # self.stopAlertor()
                # if buzzer_on==True:
                    # released = time.time()
                    # length = released - pressed							#Record length of time held fors
                    # buffer += "DASH-" if length > 0.19 else "DOT-"			
                    # answer = "DOT-DOT-DOT-DASH-DASH-DASH-DOT-DOT-DOT"		#Answer as more code in string
                    # if answer in buffer:
                        # break
                    # buzzer_on = False
            # time.sleep(0.01)
			
    def alertor(self):
         pass
        #buzz.start(50)													#Comment out for Windows testing
		
    def stopAlertor(self):
        pass
        #buzz.stop()													#Comment out for Windows testing

#Set up tkinter
root = tk.Tk()
root.title("Blitz! Control Panel")
root.resizable(width=False, height=False)

#Set up GPIO
setup()

# gameflow map on left
left_canvas = tk.Canvas(root, width=350, height=512, background="darkseagreen", borderwidth=0, highlightthickness=0)
left_canvas.grid(row=0, column=0)
left_canvas.propagate(0)

gameFlow = gameFlow(left_canvas)

# menu on right
menu_right = tk.Frame(root, width=160)
menu_right_bg_image = ImageTk.PhotoImage(Image.open("tanklight.jpg"))
menu_right_logo = ImageTk.PhotoImage(Image.open("logo.png"))

right_canvas = tk.Canvas(menu_right, borderwidth=0, highlightthickness=0)
right_canvas.create_image(0,0, image = menu_right_bg_image, anchor="nw")
right_canvas.place(x=0, y=0, relwidth=1, relheight=1)
right_canvas.create_image(60,25, image = menu_right_logo, anchor="nw")
right_canvas.create_rectangle(10, 292, 150, 502, fill="", outline="gray", width=2)

controlButtons(right_canvas)

# status bar at bottom
status_frame = tk.Frame(root)
status = tk.Label(status_frame, text="Status:")
status.pack(side=tk.LEFT)
statusUpdate = tk.Label(status_frame, text="Ready to Launch Game")
statusUpdate.pack(side=tk.LEFT)

#create grid
menu_right.grid(row=0, column=1, sticky="nsew")
left_canvas.grid(row=0, column=0, sticky="nsew") 
status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

root.grid_rowconfigure(1,weight=0)
root.grid_columnconfigure(1,weight=0)

root.mainloop()
