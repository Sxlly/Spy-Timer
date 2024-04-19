from PIL import ImageGrab, ImageTk, Image
import asyncio
import tkinter
from tkinter import messagebox
from playsound import *
import time
import customtkinter
import datetime
import threading
import pretty_errors

#*******************************
#setting default themes and apperances for customer tkinter GUI
customtkinter.set_appearance_mode("Light")
customtkinter.set_default_color_theme("dark-blue")

#Declaring App --> Title & Icon {AppBar}
SpyApp = customtkinter.CTk()
SpyApp.geometry("600x440")
SpyApp.title("Spy Timer")
SpyApp.iconbitmap("spyIcon.ico")

#/////////////////////////////////////////
#image importing and resizing 
initSpyImage = (Image.open("spyIcon.ico"))
resizedSpyImage = initSpyImage.resize((80,80))
finalSpyImage = ImageTk.PhotoImage(resizedSpyImage)

initImage = (Image.open("initIcon.ico"))
resizedInitImage = initImage.resize((20,20))
finalInitImage = ImageTk.PhotoImage(resizedInitImage)

initResetImage = (Image.open("resetIcon.ico"))
resizedResetImage = initResetImage.resize((20,20))
finalResetImage = ImageTk.PhotoImage(resizedResetImage)


#///////////////////////////////////////
#pretty errors configuration
#tkinter messagebox ERROR will be favoured over console errors 
pretty_errors.configure(
    separator_character='*',
    filename_display=pretty_errors.FILENAME_FULL,
    line_color=pretty_errors.RED + '>' + pretty_errors.default_config.line_color,
    lines_before=5,
    lines_after=5
)

#global vars 
counting = [0,0]
reset = False
timerCommand = "None"

#///////////////////////
#is Host player on Blu team detection
async def bluTeamDetector():

    image = ImageGrab.grab()
    widthStaticDimensionStart = 1187
    heightStaticDimensionStart = 20
    isOnBlu = False

    try:

        for index in range(395):

            currentPixelColor = image.getpixel((widthStaticDimensionStart + index, heightStaticDimensionStart))
            engyHelmetColorAlive = (255,217,98)
            engyHelmetColorDead = (255,205,91)


            if currentPixelColor == engyHelmetColorAlive or currentPixelColor == engyHelmetColorDead:

                print("Blu team")
                print("engineer at: " + "W:" + str(widthStaticDimensionStart + index) + " H:" + str(heightStaticDimensionStart))
                isOnBlu = True
                return isOnBlu
                
        return isOnBlu
                 
    except:
        print("AN ERROR OCCURED")   
        time.sleep(5)
        return isOnBlu

#///////////////////////
#is Host player on Red team detection
async def redTeamDetector():

    image = ImageGrab.grab()
    widthStaticDimensionStart = 1861
    heightStaticDimensionStart = 20
    isOnRed = False

    try:

        for index in range(395):

            currentPixelColor = image.getpixel((widthStaticDimensionStart + index, heightStaticDimensionStart))
            engyHelmetColorAlive = (255,205,91)
            engyHelmetColorDead = (255,217,98)

            if currentPixelColor == engyHelmetColorAlive or currentPixelColor == engyHelmetColorDead:

                print("Red Team")
                print("engineer at: " + "W:" + str(widthStaticDimensionStart + index) + " H:" + str(heightStaticDimensionStart))
                isOnRed = True
                return isOnRed

        return isOnRed

    except:
        print("AN ERROR OCCURED")
        time.sleep(5)
        return isOnRed

#///////////////////////////////////
#Locate Spys position in Hud if enemy is Red team
async def spyLocaterRed():

    image = ImageGrab.grab()
    widthStaticDimensionStart = 1861 #top left corner width pixel 
    heightStaticDimensionStart = 7 #top left corner height pixel
    spyHeadMaskColor = (55,57,55) #RGB value for SPYS head colour (his mask specifically)
    spyFaceColor = (132,132,132) #RGB value for SPYS face colour
    redBackgroundColorStatic = (78,51,49) #RGB value for the red colour in the background of all team icons in red team HUD section

    spyPixelLocation = []

    try:

        for index in range(395):

            currentPixelColor = image.getpixel((widthStaticDimensionStart + index, heightStaticDimensionStart))
            spyFaceTestPixel = image.getpixel((widthStaticDimensionStart +  index,  heightStaticDimensionStart + 2))
            backgroundTestPixel = image.getpixel((widthStaticDimensionStart - 8 + index, heightStaticDimensionStart + 2))
            print(currentPixelColor)
            print(index)

            if currentPixelColor == spyHeadMaskColor and spyFaceTestPixel == spyFaceColor and backgroundTestPixel == redBackgroundColorStatic:

                print("spy mask color: " + str(currentPixelColor))
                print("spy face color: " + str(spyFaceTestPixel))
                print("spy background colour: " + str(backgroundTestPixel))
                print("spy mask found on pixel")
                print("Width" + str(widthStaticDimensionStart + index) + "Height" + str(heightStaticDimensionStart))

                spyPixelLocation.append(widthStaticDimensionStart + index)
                spyPixelLocation.append(heightStaticDimensionStart)
                return spyPixelLocation

        return spyPixelLocation
     
    except:
        print("AN ERROR OCCURED")
        print("most likely error: SCREEN RESOLUTION SMALLER THAN CURRENT INDEX")
        time.sleep(5)
        return spyPixelLocation
    
#///////////////////////////////////
#Locate Spys position in Hud if enemy is Blu team
async def spyLocaterBlu():

    image = ImageGrab.grab()
    widthStaticDimensionStart = 1187
    heightStaticDimensionStart = 7
    spyHeadMaskColor = (59,58,59)
    spyFaceColor = (148,149,148)
    bluBackgroundColorStatic = (40,45,47)

    spyPixelLocation = []

    try:

        for index in range(395):

            currentPixelColor = image.getpixel((widthStaticDimensionStart + index, heightStaticDimensionStart))
            spyFaceTestPixel = image.getpixel((widthStaticDimensionStart + index, heightStaticDimensionStart + 2))
            backgroundTestPixel = image.getpixel((widthStaticDimensionStart + 8 + index, heightStaticDimensionStart + 2))
            print(currentPixelColor)
            print(index)


            if currentPixelColor == spyHeadMaskColor and spyFaceTestPixel == spyFaceColor and backgroundTestPixel == bluBackgroundColorStatic:

                print("spy mask color: " + str(currentPixelColor))
                print("spy face color: " + str(spyFaceTestPixel))
                print("spy background colour: " + str(backgroundTestPixel))
                print("spy mask found on pixel")
                print("Width" + str(widthStaticDimensionStart + index) + "Height" + str(heightStaticDimensionStart))

                spyPixelLocation.append(widthStaticDimensionStart + index)
                spyPixelLocation.append(heightStaticDimensionStart)
                return spyPixelLocation

        return spyPixelLocation

    except:
        print("AN ERROR OCCURED")
        print("most likely error: SCREEM RESOLUTION SMALLER THAN CURRENT INDEX")
        time.sleep(5)
        return spyPixelLocation
    
#/////////////////////////////
#determines the spys current State (Dead/Alive --> {True/False})
async def SpyState(spyLocationPixel):

    try:

        if not spyLocationPixel:
            print("Spy wasn't previously found!")
            spyStatus = "none"
            return spyStatus
        
        else:

            spyStatus = "none"
            image = ImageGrab.grab()
            color = image.getpixel((spyLocationPixel[0], spyLocationPixel[1]))

            if color == (0,0,0):

                spyStatus = "alive"
                return spyStatus

            else:
                spyStatus = "dead"
                return spyStatus
    
    except:
        print("AN ERROR OCCURED")
        print("most likely error: Pixel does not exist")
        time.sleep(5)

#//////////////////////////////////////
#sets 3rd part timer on or off {true/false} depending on spyState() method result
async def SpyTimer(spyLocationPixel):

    interation_counter = 0
    global timerCommand

    try:

        while True:

            if interation_counter == 0:

                spyStateOne = await SpyState(spyLocationPixel)
                await asyncio.sleep(0.25)
                spyStateTwo = await SpyState(spyLocationPixel)

                print("state one" + spyStateOne)
                print("state two" + spyStateTwo)

                if spyStateOne == "alive":
                    
                    interation_counter += 1
                    timerCommand = "Start"
                    aliveNoise()
                
                elif spyStateOne == "dead":
                    
                    interation_counter += 1
                    timerCommand = "Stop"
                    deathNoise()
                
                else:
                    print("There is no Spy in Play currently\n")
                    timerCommand = "Start"
                    continue
            else:

                spyStateOne = await SpyState(spyLocationPixel)
                await asyncio.sleep(0.25)
                spyStateTwo = await SpyState(spyLocationPixel)

                print("state one" + spyStateOne)
                print("state two" + spyStateTwo)

                if spyStateOne == "dead" and spyStateTwo == "alive":

                    timerCommand = "Start"
                    aliveNoise()

                elif spyStateOne == "alive" and spyStateTwo == "dead":
                    
                    timerCommand = "Stop"
                    deathNoise()
                
                else:
                    continue
    except:
        print("AN ERROR OCCURED")
        time.sleep(5)

#///////////////////////////////
#sound cue played to user when the spy spawns and timer starts --> through .wav file in a file PATH location
async def aliveNoise():

    iteration_counter = 0

    while iteration_counter == 0:

        playsound("**ADD FILE PATH HERE OF SOUND YOUD LIKE TO USE") #this will throw an ERROR if not changed to actual file PATH**
        iteration_counter += 1
    
    return

#////////////////////////////
#sound cue played to user when the spy dies and timer starts --> through .wav file in a file PATH location
async def deathNoise():

    iteration_counter = 0

    while iteration_counter == 0:

        playsound("**ADD FILE PATH HERE OF SOUND YOUD LIKE TO USE") #this will throw an ERROR if not changed to actual file PATH**
        iteration_counter += 1
    
    return


#///////////////////////////////
#method to count upwards on timer, displayed via text on app face
def counter():

    global counting, reset, timerCommand

    if timerCommand == 'Start':
        counting[0] += 1

        if counting[0] == 100:
            counting[1] += 1
            counting[0] = 0
            counting_label.configure(text = f'{datetime.timedelta(seconds=counting[1])}: 00')

        else:
            counting_label.configure(text= f'{datetime.timedelta(seconds=counting[1])}: {counting[0]}')

    if timerCommand == 'Stop':

        reset = False
        counting = [0,0]
        counting_label.configure(text="0:00:00:00")
    
    
    elif reset:
        reset = False
        counting = [0, 0]
        counting_label.configure(text="0:00:00:00")
    
    SpyApp.after(5, counter)

#///////////////////////////////
#method to change timer status determined on user interaction {input} ==> button pressed changes timer status ==> displayed via text on app face
def countup_method(command):

    global reset

    if command == 'reset':

        reset_btn.configure(text="Reset")
        reset = True
    
    elif command == 'run':

        initTimer_btn.configure(text='Initialise', command=lambda: initialise_Timer())
        counter()

#////////////////////
#main function ---> run function
async def main():

    #1 --> Run team detection
    #asynchronous
    #2 --> Run Spy location in 9v9 hud detection
    #asynchronous
    #3 ---> Run spy state (Dead/Alive {True/False}) detection 
    #4 --> Run #3 While True (forever unless error FLAG or terminal kill)
    try:

        #1
        hostOnBlu = await bluTeamDetector()

        if hostOnBlu == True:
            
            #2
            spyPixel = await spyLocaterRed()

            #3 --> #4
            await SpyTimer(spyPixel)
            return
        
        else:

            #2
            spyPixel = await spyLocaterBlu()

            #3 --> #4
            await SpyTimer(spyPixel)
            return
        
    except:
        print("AN ERROR OCCURED")
        flagError()
        time.sleep(5)


    return


#///////////////////////////////
#show ERRORMESSAGE method ---> Custom Tkinter GUI
def flagError():
    messagebox.showerror(title="Error", message="Spy Timer has accounted the following error: ")

#///////////////////////////////
#main run method wrapper method
async def main_runner():

    await main() #<--- RUN main function for spyScript


#////////////////////////////////
##asyncio between callback buffer method --> RUNS in between thread call and asynchronous method
def between_thread():

    loop = asyncio.new_event_loop() # <--- create new asynchronous loop
    asyncio.set_event_loop(loop) # <--- set new event loop to current event loop

    loop.run_until_complete(main_runner()) #<--- run the event loop until complete (nevers completes as has an infinite loop inside main())
    loop.close()


#////////////////////////////////
##initialise program method --> RUNS when init button is pressed which RUNS --> second thread for live GUI updating
def initialise_Timer():

    continous_timer_thread = threading.Thread(target= between_thread, args=()) # <--- thread creation
    continous_timer_thread.start()

    return


#Styling GUI SECTION***
# interface layout and packing (pushing to app) =>>>

#bgimage
bgImg = ImageTk.PhotoImage(Image.open("tf2spybg_resized.jpg"))
bgLayout = customtkinter.CTkLabel(master=SpyApp, image=bgImg)
bgLayout.pack()

#timerUIFrame => everything inside this frame***
frame = customtkinter.CTkFrame(master=bgLayout, width=320, height=360, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

titleImage = customtkinter.CTkLabel(master=frame, text="", image=finalSpyImage)
titleImage.place(x=120, y=25)

counting_label = customtkinter.CTkLabel(master=frame, width=220, text="0:00:00:00", font=("Century Gothic", 25))
counting_label.place(x=50, y=110)

reset_btn = customtkinter.CTkButton(master=frame, width=220, text="Reset", image=finalResetImage, font=("Century Gothic", 20), corner_radius=6, fg_color="#8f8e8b", command=lambda: countup_method('reset'))
reset_btn.place(x=50, y=160)

initTimer_btn = customtkinter.CTkButton(master=frame, width=220, text="Initialise", image=finalInitImage, font=("Century Gothic", 20), corner_radius=6, fg_color="#8f8e8b", command=lambda: countup_method('run'))
initTimer_btn.place(x=50, y=200)

#RUN APP --->>>
#/*************\
if __name__ == "__main__":
    SpyApp.mainloop()








