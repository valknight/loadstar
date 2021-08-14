import loadstar.cookstar
import loadstar.ui
from loadstar.log import Log
from multiprocessing import Process, Manager

if __name__ == '__main__':
    
    # create our Manager
    manager = Manager()
    # create our datastore
    ds = manager.dict()
    p_c = Process(target = loadstar.cookstar.start, args = (ds, ))
    p_s = Process(target = loadstar.ui.start, args = (ds, ))
    
    ds['hide_console'] = True
    ds['log'] = Log()
    p_c.start()
    p_s.start()
    p_c.join()
    