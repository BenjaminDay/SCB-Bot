from pyautogui import * 
import pyautogui 
import time 
import keyboard 
import random
import win32api, win32con

mainloop = True


while mainloop!= False:
    if pyautogui.locateOnScreen('steam test.png', region=(0,0,1920,1080), grayscale=True, confidence=0.8) != None:
        print("I can see it")
        time.sleep(0.5)
    else:
        print("I am unable to see it")
        time.sleep(0.5)
