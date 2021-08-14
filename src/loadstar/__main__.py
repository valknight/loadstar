
from loadstar.cookstar import Cookstar
from threading import Thread
from datetime import datetime
import time

c = Cookstar()
def cStarLoop():
    while True:
        c.loop()

cookstar_loop = Thread(target=cStarLoop)

def second():
    while True:
        print(datetime.now().strftime("%H:%M:%S"))
        time.sleep(1)
s = Thread(target=second)

if __name__ == '__main__':
    s.start()
    cookstar_loop.start()