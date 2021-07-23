import time

eta = time.time() + 10
factories = []
mainloop = True
while mainloop:
    print(time.time())
    if time.time() >= eta:
	    mainloop = False
