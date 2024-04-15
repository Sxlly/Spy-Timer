from PIL import ImageGrab
import pyautogui
import asyncio
import time
from tkinter import *
from tkinter import messagebox
from playsound import *

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
            engyHelmetColor = (255,217,98)


            if currentPixelColor == engyHelmetColor:

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
            engyHelmetColor = (255,205,91)

            if currentPixelColor == engyHelmetColor:

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

    try:

        while True:

            if interation_counter == 0:

                spyStateOne = await SpyState(spyLocationPixel)
                await asyncio.sleep(0.25)
                spyStateTwo = await SpyState(spyLocationPixel)

                print("state one" + spyStateOne)
                print("state two" + spyStateTwo)

                if spyStateOne == "alive":

                    pyautogui.press('o')
                    interation_counter += 1
                    aliveNoise()
                
                elif spyStateOne == "dead":

                    pyautogui.press('p')
                    interation_counter += 1
                    deathNoise()
                
                else:
                    print("There is no Spy in Play currently\n")
                    continue
            else:

                spyStateOne = await SpyState(spyLocationPixel)
                await asyncio.sleep(0.25)
                spyStateTwo = await SpyState(spyLocationPixel)

                print("state one" + spyStateOne)
                print("state two" + spyStateTwo)

                if spyStateOne == "dead" and spyStateTwo == "alive":

                    pyautogui.press('o')
                    aliveNoise()

                elif spyStateOne == "alive" and spyStateTwo == "dead":

                    pyautogui.press('p')
                    deathNoise()
                
                else:
                    continue
    except:
        print("AN ERROR OCCURED")
        time.sleep(5)

async def aliveNoise():

    interation_counter = 0

    while interation_counter == 0:

        playsound("C:\Users\shaes\OneDrive\Desktop\Lego_yoda_death_sound.wav")
        interation_counter += 1

    return

async def deathNoise():

    interaction_counter = 0

    while interaction_counter == 0:

        playsound("C:\Users\shaes\OneDrive\Desktop\alive.wav")
        interaction_counter += 1

    return


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
        time.sleep(5)

    return


#///////////////////
#Run Method ---> Script calls main()
async def run_method():

    await main()
    return

#!//////!
#Run Call
asyncio.run(main())




