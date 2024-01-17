import asyncio, asyncvnc
from PIL import Image
import time
import random



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
        #coordinates.append
        return coordinates

    def posToCoord(self, pos2D):
        #convert positions to coords
        coords = []

        for i in pos2D: 
            coords.append([self.startX + self.buttonWidth * i[0], self.startY + self.buttonHeight * i[1]])
        return coords


if __name__ ==  "__main__":

    #distace between lock-screen button centers
    buttonWidth = 275
    buttonHeight = 260

    #offset
    keypadpos = [270, 1150]

    file = open("password.txt", "r")
    password = file.readline()

    pad = Keypad(keypadpos[0], keypadpos[1], buttonWidth, buttonHeight, password)


    async def run_client():
        async with asyncvnc.connect('192.168.0.149') as client:
        
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
                
                #client.mouse.scroll_down()
                
                #click(610, 1920,0.5)
                #click(630, 1950,0.5)
                #with client.mouse.hold():
                #    time.sleep(1)
                time.sleep(1.5)
                #click(610, 1700,1)

            click(random.randint(700, 800), random.randint(1900, 2000), 1)
            time.sleep(0.2)
            print("wakeup")
            #wakeUp()
            print("startclash")
            startClash()
            
            time.sleep(1)

            #write code
            for i in pad.posToCoord(pad.getpos()):
                click(i[0], i[1], 0.2)

            time.sleep(7)
            x = time.time()
            pixels = await client.screenshot()
            print(time.time() - x)
            # Save as PNG using PIL/pillow
            image = Image.fromarray(pixels)
            image = image.crop((40, 2180, 1050,2200))
            image.show()
            #image.save('screenshot.png')
                
            

    asyncio.run(run_client())
