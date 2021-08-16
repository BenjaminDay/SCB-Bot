import pyautogui, keyboard, win32api, win32con, win32gui, cv2, subprocess, random, numpy as np, ast
from time import time, sleep
from image_rec_tester import get_image_pos, relative, convert_xy_wh
from text_rec_tester import get_text

"""
Run process:

Boot NoxPlayer and locate game icon
Startup game - check if game is loaded
Run get button coords for bot, get_stats to fetch player data and load data related to the player's level
Get inventory data
Reset Camera pos
Confirm depo location and get status
Find factory and commercial buildings and get statuses
find tax building
# later - determine shortest path between buildings
get harbor location, status and requirements
calculate next step and add it to the process queue list
execute next step in queue
run until keyboard interrupt
"""

"""
Todo:

Write click_rel to handle a reference as input for relative clicks
"""

#string = get_text(preset, reference) #preset is a tuple x1, y1, w, h for a region on the screen relative to the game window


class CustomError(Exception):
    pass

try:
    with open('presets.txt','r') as f:
        PRESET = ast.literal_eval(f.read())
except:
    CustomError('Presets.txt - file does not exist')

#Button class stores data about the buttons used for the code. It collects the button location using a preset location relative to the window
#this enables the class to be used again in case the window is repositioned. Also it executes the clicks for the buttons.
class Button:
    def __init__(self, filepath, image, preset, reference):
        self.fp = filepath
        self.image = image
        self.preset = relative(preset[:2], reference, "to00")+preset[2:] #relative preset gets converted into real coordinates for later use

    def get_button(self):
        self.pos = get_image_pos(self.fp, self.image, self.preset) #returns a real xy coord with wh
        if self.pos != None:
            self.pos = centre(self.pos)

    def click_button(self):
        click(self.pos)

#Presses the esc key
def esc():
    keyboard.press_and_release('esc')
    sleep(1)

#Takes a 4 length input tuple and outputs a 2 length tuple (point) being the centre
def centre(in_tuple)-> tuple:
    x, y, w, h = in_tuple
    return (x + w // 2, y + h // 2)

#Normal left mouse down+up event
def click(point):
    pyautogui.moveTo(point[0], point[1], round(random.uniform(0.14, 0.17), 3))  #Moves mouse to point at a random speed between 0.14s and 0.17s
    sleep(0.05)
    pyautogui.click(button = 'left')

#Drags left mouse from point1 to point2
def drag(point1, point2):
    pyautogui.moveTo(point1[0], point1[1], round(random.uniform(0.14, 0.17), 3))
    sleep(0.1)
    pyautogui.dragTo(point2[0], point2[1], round(random.uniform(0.94, 0.97)), button='left')

#Checks if the game has loaded and returns as soon as it sees the target images
def is_loaded(button_name, loops = 120, delay = 0.5)-> bool:  #Returns T/F depending if the images appear on the screen
    for x in range(0, loops):
        if x % 5 == 0:
            print("Loading...")
        button_name.get_button()
        if button_name.pos != None:
            print("Loaded!")
            return True
        sleep(delay)
    return False

#Booting Nox emulator, then opening game after icon is detected post loading screen
def boot_nox():  #No returns, just code to interact with globals and execute startup
    print("Boot start") ##-
    subprocess.Popen([r"C:\Program Files (x86)\Nox\bin\Nox.exe", r"-clone:Nox_1"])
    sleep(2)

    #Assigning default values for the bot to stay confined in during the process of operating
    global window_xy, window_wh
    print("Getting window dimensions and position...") ##-
    window_xy = win32gui.GetWindowRect(win32gui.FindWindow(None, "Feeder 1"))
    window_xy = (window_xy[0]+8, window_xy[1]+30, window_xy[2]-8, window_xy[3]-8) #Adjusting for Windows invisible pixel border (8 pixels) and header bar (30 pixels)
    window_wh = convert_xy_wh(window_xy)
    print("Window dimensions got.") ##-
    print(f"window xy: {window_xy} and wh: {window_wh}") ##-

    sleep(1)
    print("Checking if emulator is loaded...") ##-
    game_exe = Button("images/buttons/", "exe", PRESET['exe'], window_xy[:2])
    state = is_loaded(game_exe)
    print(f"boot - Is emulator loaded? {state}") ##-
    if game_exe.pos != None:
        print("Launching game...") ##-
        game_exe.click_button()
        print("Checking if game loaded:") ##-
        house = Button("images/buttons/", "house", PRESET['bottom right menu'], window_xy[:2])
        state = is_loaded(house)
        print(f"boot - Is city loaded? {state}") ##-
        sleep(0.05)
        print("Boot end") ##-
    else:
        raise CustomError('Not Booted')

#Converts a string storing time information into seconds
def get_time(text)->int:
    time = 0
    buffer = ""
    for letter in text:
        if letter == "h":
            time += int(buffer)*3600
            buffer = ""
        elif letter == "m":
            time += int(buffer)*60
            buffer = ""
        elif letter == "s":
            time += int(buffer)
            buffer = ""
        if letter.isdigit():
            buffer += letter
    return time

#Collects daily chest information, checks if it needs to be claimed and claims if needed. Returns the time remaining till next claim
def get_dc_info(button_name, ref):
    print("Checking daily chest...") ##-
    text = get_text(PRESET['claim check'], ref)
    if text == "Bonus Chest is":
        print("Ready to claim!") ##-
        claim.click_button()
        sleep(7)
        shop.click_button()
        sleep(1)
    print("Daily chest claimed.") ##-
    text = get_text(PRESET['daily time'], ref)
    dc_time = get_time(text)
    if dc_time > 3600:
        print(f"Time until next claim: {dc_time//3600} hours and {dc_time//60%60} minutes...") ##-
    else:
        print(f"Time until next claim: {dc_time//60%60} minutes and {dc_time%60} seconds...") ##-
    esc()
    return dc_time


def setup(reference):
    print("Setup start") ##-
    global friends, daniel, home, house, storage, shop, claim, commercial, factory, servandspec, gov
    print("Getting buttons...") ##-
    friends = Button("images/buttons/", "friends", PRESET['bottom left menu'], reference)
    friends.get_button()
    print("Friends menu got:", friends.pos) ##-
    friends.click_button()
    sleep(1)
    daniel = Button("images/buttons/", "daniel", PRESET['friends list'], reference)
    daniel.get_button()
    print("Daniels got:", daniel.pos) ##-
    daniel.click_button()
    home = Button("images/buttons/", "home", PRESET['home'], reference)
    state = is_loaded(home) #Checks if the home button to return to the players city is present
    print(f"setup - Is daniels loaded? {state}") ##-
    print("Home got:", home.pos) ##-
    home.click_button()
    house = Button("images/buttons/", "house", PRESET['bottom right menu'], reference)
    state = is_loaded(house) #Checks if the player city is laoded
    print(f"boot - Is city loaded? {state}") ##-
    print("House got:", house.pos) ##-
    storage = Button("images/buttons/", "storage", PRESET['storage icon'], reference)
    storage.get_button()
    print("Storage got:", storage.pos) ##-
    shop = Button("images/buttons/", "shop", PRESET['simcash shop'], reference)
    shop.get_button()
    print("Shop got:", shop.pos) ##-
    shop.click_button()
    sleep(1)
    claim = Button("images/buttons/", "claim", PRESET['daily chest'], reference)
    claim.get_button()
    get_dc_info(claim, reference)
    commercial = Button("images/buttons/", "commercial", PRESET['bottom right menu'], reference)
    commercial.get_button()
    print("Commercial got:", commercial.pos) ##-
    factory = Button("images/buttons/", "factory", PRESET['bottom right menu'], reference)
    factory.get_button()
    print("Factory got:", factory.pos) ##-
    servandspec = Button("images/buttons/", "servandspec", PRESET['bottom right menu'], reference)
    servandspec.get_button()
    print("Services and Specs got:", servandspec.pos) ##-
    servandspec.click_button()
    sleep(1)
    gov = Button("images/buttons/", "gov", PRESET['services and specs'], reference)
    gov.get_button()
    print("Government got:", gov.pos) ##-
    esc()
    print("Setup end") ##-

#Reset camera positioning in game
def reset_cam_pos():
    pass

if __name__ == '__main__':
    boot_nox()
    setup(window_xy[:2])
