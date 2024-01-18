
import asyncio, asyncvnc
from PIL import Image
import time
ip = "192.168.0.149"


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
                
                #client.mouse.scroll_down()
                
                #click(610, 1920,0.5)
                #click(630, 1950,0.5)
                #with client.mouse.hold():
                #    time.sleep(1)
                time.sleep(1.5)
                #click(610, 1700,1)

            
        
            

           
            pixels = await client.screenshot()
            
            # Save as PNG using PIL/pillow
            image = Image.fromarray(pixels)
            image = image.crop((40, 2190, 1050,2200))
            chests = []

            for i in range(4):
                chest = image.crop((image.size[0]/4 * i,0, image.size[0]/4 * (i+1), image.size[1]))
                chests.append(chest)

            for i in chests:
                i = i.crop((i.size[0]/4, 0, i.size[0]/4 * 3, i.size[1]))
                i.show()

          
            # width, height = RGBimage.size
            # for i in range(width):
            #     for j in range(height):
            #         if i == 5:
            #             print(RGBimage.getpixel((i,j))) 

            # image.show()
            #image.save('screenshot.png')
                
            

asyncio.run(run_client())


