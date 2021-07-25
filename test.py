import pytesseract
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import cv2
import numpy as np

def click(xy):
    win32api.SetCursorPos(xy)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01) #This pauses the script for 0.01 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)

def drag_click(start, finish):
    win32api.SetCursorPos(start)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1) #This pauses the script for 0.01 seconds
    win32api.SetCursorPos(finish)
    time.sleep(0.1) #This pauses the script for 0.01 seconds
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)


print("Executing in 2 seconds...")
time.sleep(1)
print("Executing in 1 seconds...")
time.sleep(1)
print("Executing.")
drag_click((540, 342), (540, 63))
