import loadstar.cookstar
import loadstar.ui
import webbrowser
import sys
import time
from loadstar.log import Log
from multiprocessing import Process, Manager, freeze_support

if __name__ == '__main__':
    freeze_support()
    # create our Manager
    manager = Manager()
    # create our datastore
    ds = manager.dict()
    p_c = Process(target = loadstar.cookstar.start, args = (ds, ))
    p_s = Process(target = loadstar.ui.start, args = (ds, ))
    ds['hide_console'] = False
    ds['log'] = Log()
    ds['livesplit_connected'] = True
    p_c.start()
    p_s.start()
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:10000/')
    p_c.join()
    p_c.terminate()
    p_s.terminate()
    print('Quit!')
    sys.exit(0)
