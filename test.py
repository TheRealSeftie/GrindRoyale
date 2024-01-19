import asyncio, asyncvnc
from PIL import Image
from time import sleep
from random import randint
import numpy as np
from  matplotlib import pyplot as plt


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
    
    ip = "192.168.200.231"
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

            
                        

            
            pixels = await client.screenshot()
                
            #image = Image.fromarray(pixels)

            fullchest = Image.fromarray(pixels)


            fullchest = fullchest.crop((0, client.video.height/100*80, client.video.width, client.video.height/100*92))
            chests = []
            for i in range(4):
                    chest = fullchest.crop((fullchest.size[0]/4 * i,0, fullchest.size[0]/4 * (i+1), fullchest.size[1]))
                    chests.append(chest)
                    
            slotcenter = []
            for chest in chests:
                slotcenter.append(chest.crop((chest.size[0]/2 - 5, chest.size[1] / 2 -5, chest.size[0]/2 + 5, chest.size[1] / 2 + 5)))

            for slot in slotcenter:
                slot.show()
            

                
           
            

    asyncio.run(run_client())
