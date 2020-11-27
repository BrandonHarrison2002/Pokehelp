import numpy as np
from PIL import ImageGrab, Image
import cv2
import pytesseract
from playsound import playsound
from pynput.keyboard import Key, Controller
import pyautogui


move = False
fight = True
killlist = ['oddish', 'gloom', 'natu', 'duduo', 'dodrio', 'pidgeotto']
catchlist = ["riolu", "hippopotas"]


class Cord:
    def __init__(self, x=0, y=0, offx=100, offy=100):
        self.x = x
        self.y = y
        self.offx = offx
        self.offy = offy
    
    def grab(self):
        return ImageGrab.grab(bbox=(self.x, self.y, self.x + self.offx, self.y + self.offy)).convert('L')


class Process:
    def __init__(self):
        self.lastpokemon = "unknown"
        self.ocrErr = False
        self.keyboard = Controller()
        self.left = False

    def processImg(self, greyImg):
        txt = pytesseract.image_to_string(greyImg)
        for pokemon in catchlist:
            if txt.lower().find(pokemon) > -1:
                self.lastpokemon = pokemon
                return 1
        for pokemon in killlist:
            if txt.lower().find(pokemon) > -1:
                self.lastpokemon = pokemon
                return 2
        return 0
    
    def found(self):
        print('Found')
        playsound('Found.wav')

    def search(self, greyImg):
        txt = pytesseract.image_to_string(greyImg)
        if txt == None or len(txt) <= 1:
            if move:
                print('Moving')
                if self.left:
                    self.left = False
                    self.keyboard.press('a')
                    self.keyboard.release('a')
                else:
                    self.left = True
                    self.keyboard.press('d')
                    self.keyboard.release('d')
        else:
            print('Escaping')
            self.keyboard.press('4')
            self.keyboard.release('4')
    
    def fight(self, greyImg):
        txt = pytesseract.image_to_string(greyImg)
        self.keyboard.press('1')
        self.keyboard.release('1')
        # if txt.lower().find('choose attack') > -1:
        #     print('waiting')
        # else:
        #     self.keyboard.press('1')
        #     self.keyboard.release('1')
        print('Fighting')



def main():
    process = Process()
    while(True):
        battle = Cord(760,415,1030,600)
        wild = Cord(1195,433,210,40)
        chooseAttack = Cord(1555,780,200,30)

        img = wild.grab()
        atk = chooseAttack.grab()
        
        img = np.array(img)
        atk = np.array(atk)
        cv2.imshow('window', img)
        
        if process.processImg(img) == 1:  
            process.found()
        elif process.processImg(img) == 2 and fight:
            process.fight(atk)
        else:
            process.search(img)

        if cv2.waitKey(25) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()

