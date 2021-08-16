import win32gui

"""
This program allows the collection of coordinate presets and storage for the bot to have a smaller area on the screen to check for buttons in the main program

How to use:

Open up the android emulator and launch the app.
When you are ready, press "r" to record the position of your mouse as a coordinate, once you have 2 coordinates, press "s" to submit your recorded coordinates with a tag into a dictionary.
You can also press "d" to delete the last coordinate recorded and not yet submitted.
Finally press "q" to close the program. This will write the dictionary to a .txt file for the main program to read.

"""

"""
Process:
Check for keyboard input, if "r" get current mouse pos and add it to point tuple
if "s" take point and take input then add it to presets dict
if "d" delete last item in point tuple if not empty
if "q" write dict to txt and quit.
"""


#Converts coords between (0, 0) reference frame and a window
def relative(point, reference, mode = "from00")-> tuple: #Returns same lenght tuple inputted as point
    if len(point) % 2 == 1:
        raise CustomError('relative - tuple point must have an even number of items')
    if len(point) > 2:
        return (relative(point[:2], reference, mode) + relative(point[2:], reference, mode))  #Recursive call if the length of point is more than 2 that then concatenates tuples on the way up
    if mode == "from00":  #Converts real point to be relative to reference
        return (point[0] - reference[0], point[1] - reference[1])  #e.g. point (110, 150) turns into (10, 25) with reference (100, 125)
    elif mode == "to00":  #Converts a relative to be a real value relative to (0, 0)
        return (point[0] + reference[0], point[1] + reference[1])  #e.g. point (10, 25) turns into (110, 150) from reference (100, 125)


def main(window_title):
    print("You can 'r' - to record, 'd' - delete last point recorded, 's' - store recorded points, 'p' - pop last stored, 'q' - quit and submit the stored values to a text document.\n")
    window_dim = win32gui.GetWindowRect(win32gui.FindWindow(None, window_title))  #x1, y1, x2, y2
    window_tl = (window_dim[0]+8, window_dim[1]+30)
    print(f"Reference: {window_tl}")

    presets = {}
    mainloop = True
    box = None
    while mainloop:
        print(f"Box: {box}")
        mode = input("Waiting for input: 'r', 's', 'd', 'p', 'q'\n")
        window_dim = win32gui.GetWindowRect(win32gui.FindWindow(None, window_title))  #x1, y1, x2, y2
        window_tl = (window_dim[0]+8, window_dim[1]+30)
        if mode == 'r':
            if box == None:
                box = relative(win32gui.GetCursorPos(), window_tl)
            elif len(box) == 2:
                box += relative(win32gui.GetCursorPos(), relative(box[:2], window_tl, "to00"))
            else:
                print("You already have two points stored")
        elif mode == 's':
            if len(box) == 4:
                tag = input('Name your preset:\n')
                presets[tag] = box
                box = None
                print(f"Presets: {presets}")
            else:
                print("You need to have 2 points to store a preset")
        elif mode == 'd':
            if box != None:
                if len(box) == 4:
                    box = box[:2]
                else:
                    box = None
            else:
                print("Nothing to delete")
        elif mode == 'p':
            if len(presets) > 0:
                presets.popitem()
                print(f"Presets: {presets}")
            else:
                print("Nothing to delete")
        elif mode == 'q':
            f = open("presets.txt", "a")
            f.write(str(presets))
            f.close()
            mainloop = False
        else:
            print("Unrecognised")
    #while 1:
        #print(f"real : {win32gui.GetCursorPos()} relative: {relative(win32gui.GetCursorPos(), reference)}")
    print("Exit")

if __name__ == '__main__':

    """Edit window_title to whatever your emulator is called"""

    window_title = "Feeder 1"
    main(window_title)
