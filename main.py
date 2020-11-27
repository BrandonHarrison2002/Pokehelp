import numpy as np
from PIL import ImageGrab, Image
import cv2
import pytesseract
from playsound import playsound
from pynput.keyboard import Key, Controller
import pyautogui



catchlist = ["gible"]

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
                return True
    
    def search(self, greyImg):
        txt = pytesseract.image_to_string(greyImg)
        if txt == None or len(txt) <= 1:
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
    


def main():
    process = Process()
    while(True):
        battle = Cord(760,415,1030,600)
        # Wild = Cord(1195,433,210,40)
        wild = Cord(pyautogui.size()[0]/2.1422594142259412, pyautogui.size()[1]/3.325635103926097, pyautogui.size()[0]/12.19047619047619, pyautogui.size()[1]/36.0)

        img = wild.grab()
        
        img = np.array(img)
        cv2.imshow('window', img)
        
        if process.processImg(img):  
            print('Found')
            playsound('Found.wav')
        else:
            process.search(img)



        if cv2.waitKey(25) & 0xFF == ord('q'):  
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    main()

