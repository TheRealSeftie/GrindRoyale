import asyncio, asyncvnc
from PIL import Image
import time
import random
import numpy as np

class Keypad:
    def __init__(self, startX, startY, buttonWidth, buttonHeight, code):
        self.startX = startX
        self.startY = startY
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight
        self.code = code
        self.buttons =              [[1, 2, 3],
                                    [4, 5, 6],
                                    [7 ,8 ,9],
                                    ["b",0, "e"] ]

    def getpos(self, code=None):
        #convert code to positions

        coordinates = []
        if code == None:
            code = self.code

        for i in str(code):
            for j in self.buttons:
                for k in j:
                    if str(k) == i:
                        coordinates.append([j.index(k),self.buttons.index(j)])
        return coordinates

    def posToCoord(self, pos2D):
        #convert positions to coords
        coords = []

        for i in pos2D: 
            coords.append([self.startX + self.buttonWidth * i[0], self.startY + self.buttonHeight * i[1]])
        return coords


if __name__ ==  "__main__":
    
    ip = "192.168.0.149"
    #distace between lock-screen button centers
    buttonWidth = 275
    buttonHeight = 260

    #offset
    keypadpos = [270, 1150]

    file = open("password.txt", "r")
    password = file.readline()

    pad = Keypad(keypadpos[0], keypadpos[1], buttonWidth, buttonHeight, password)


    async def run_client():
        async with asyncvnc.connect(ip) as client:
        
            def click(x, y, duration=0):
                client.mouse.move(x, y)
                client.mouse.click()
                time.sleep(duration)

            def startClash():

                #quick settings menu
                client.mouse.move(500,0)
                client.mouse.scroll_up()
                time.sleep(0.5)

                #click quick setting
                client.mouse.move(800,1300)
                with client.mouse.hold():
                    time.sleep(1)

            def wakeUp():
                for i in range(2):
                    # 270 1600 
                    # 800 2000
                    click(random.randint(700, 800), random.randint(1900, 2000), 1)
                
                time.sleep(1.5)
            
            async def getChestbars():
                
                #get image of chest row
                pixels = await client.screenshot()
                image = Image.fromarray(pixels)
                fullchest = Image.fromarray(pixels)
                image = image.crop((0, client.video.height/100*91.5, client.video.width, client.video.height/100*92))
                
                chests = []
                #cut to four images
                for i in range(4):
                    chest = image.crop((image.size[0]/4 * i,0, image.size[0]/4 * (i+1), image.size[1]))
                    chests.append(chest)

                #crop each image even more
                for i in chests:
                    chests[chests.index(i)] = i.crop((i.size[0] / 4, 0, i.size[0] / 4 * 3, i.size[1]))

                return chests

            async def getChestCenter():
                #fullchest for difference between unopened and empty slot
                pixels = await client.screenshot()
                fullchest = Image.fromarray(pixels)

                fullchest = fullchest.crop((0, client.video.height/100*80, client.video.width, client.video.height/100*92))
                chests = []
                for i in range(4):
                        chest = fullchest.crop((fullchest.size[0]/4 * i,0, fullchest.size[0]/4 * (i+1), fullchest.size[1]))
                        chests.append(chest)
                        
                slotcenter = []
                for chest in chests:
                    slotcenter.append(chest.crop((chest.size[0]/2 - 5, chest.size[1] / 2 -5, chest.size[0]/2 + 5, chest.size[1] / 2 + 5)))
                return slotcenter

        


            def getAverageColour(i):
                #get average colours of each image
               
                colours = []
                
                colour = [0,0,0]
                for row in range(i.width):
                    for column in range(i.height):
                        for pixelcolour in range(len(colour)):
                            colour[pixelcolour] += i.getpixel((row,column))[pixelcolour]

                    for j in range(len(colour)):
                        colour[j] /= row + 1

                colours.append([round(colour[0]),round(colour[1]),round(colour[2])])

                #get "lagom" enough colour
                return colours

            async def RGBtoText(colours):
                words = []
                for colour in colours:
                    if np.sum(np.abs(np.subtract(colour, [5,16,9]))) < 5:
                        words.append("GREEN")
                    elif np.sum(np.abs(np.subtract(colour, [17,11,3]))) < 5 or np.sum(np.abs(np.subtract(colour, [19,13,4]))) < 5 or np.sum(np.abs(np.subtract(colour, [15,9,2]))) < 5 or np.sum(np.abs(np.subtract(colour, [12,7,2]))) < 5:
                        words.append("YELLOW")
                    elif np.sum(np.abs(np.subtract(colour, [14,8,20]))) < 7:
                        #words.append("CLEAR")
                        slotcenter = await getChestCenter()
                        
                        #print(await RGBtoText(getAverageColour()))

                        
                        if np.sum(np.abs(np.subtract(getAverageColour(slotcenter[colours.index(colour)]), [64,28,133]))) < 5 :
                            words.append("EMPTY")
                        else:
                            words.append("CHEST")

                    else:
                        words.append("IDK")
                        return False
                return words

            async def recursion():
                colours = await getChestColour()
                if RGBtoText(colours):
                    return RGBtoText(colours)
                else: await recursion()


            #--------------MAIN------------------

            #wakeup
            click(random.randint(700, 800), random.randint(1900, 2000), 1)
            time.sleep(0.2)
            
            startClash()
            
            time.sleep(1)

            #write code
            for i in pad.posToCoord(pad.getpos()):
                click(i[0], i[1], 0.3)

            time.sleep(2)

            status = []
            while True:
                bars = await getChestbars()
                colours = []
                for image in bars:
                    colours.append(getAverageColour(image))

                if await RGBtoText(colours):
                    status = await RGBtoText(colours)
                    break
                time.sleep(0.5)
                
            print(status)

            if "GREEN" in status:
                print("I SHOULD KILL MYSELF")
                
                

            elif "CHEST" in status:
                
                click(int(client.video.width/4 * status.index("CHEST") + client.video.width/8), int(client.video.height/100 * 85), 1)

                click(int(client.video.width/100 * 50), int(client.video.height/100*71))
    #550 1750
            
    asyncio.run(run_client())
