import cv2
import livesplit
import click
import sys
import time
from loadstar.fps import FPSCounter
from loadstar.console import ConsoleUI
from loadstar.camera import CamFinder, NoMoreCamerasException
from loadstar.analysis import checkIfLoading
from loadstar.log import Severity, Log


class Cookstar():
    def __init__(self):
        self._livesplitConnection = None
        self._cam = None
        self.fps = FPSCounter()
        self.finder = CamFinder()
        self.wasPaused = False
        self.loading = False
        self.console_enabled = True
        self.ui = ConsoleUI()
        self.lastCheckLoad = False
        self.frame = None
        # Shim datastore - overwrite this if you have a proper one!
        self.ds = dict()
        self.ds['log'] = Log() 

        # this is black enough for most capture cards, you shouldn't need to calibrate this!
        # if you DO need to regularly calibrate, that's a good sign the colours are off in your capture card
        self.loadingColour = 10
        # allow two either side of the loadingColour (IE: if loading colour is 3, and range is 2, loading colours are defined as between 1 and 5 inclusive)
        self.colourRange = self.loadingColour

        # Performance / Accuracy
        # max = 100, min = 1
        # number of pixels to skip
        self.pixelsToSkip = 100
        # TODO: Use clamping function for this.
        if self.pixelsToSkip > 100:
            pixelsToSkip = 100
        elif self.pixelsToSkip < 1:
            pixelsToSkip = 1

        # Set this as low as you can without causing performance issues - having it higher may lead to frames either being counted incorrectly.
        # It shouldn't have an impact if at 2 or 3 over a long run, but for short runs you need to keep this in mind
        self.frameInterval = 2
        self.displayFrame = 0
        self.frameTimer = 0

    @property
    def livesplit(self):
        if self._livesplitConnection is None:
            self._livesplitConnection = livesplit.Livesplit(
                setupGameTimer=True)
        return self._livesplitConnection

    @property
    def cam(self) -> cv2.VideoCapture:
        if self._cam is None:
            try:
                self._cam = self.finder.cam
            except NoMoreCamerasException:
                # TODO: Replace with logging!
                self.ds['log'] = self.ds['log'].error("Ran out of cameras! Check OBS VirtualCam is working right.")
                #cv2.destroyAllWindows()
                #sys.exit(1)
        return self._cam

    def markCamAsBorked(self):
        """Does what it says on the tin - marks the current camera in use as not working, and will cause a new camera to be found next time .cam is requested
        Can also be used if you just... want a new camera!
        """
        self.ds['log'] = self.ds['log'].warn('Camera {} was marked as borked. Releasing it!'.format(self.finder.camIndex))
        self.cam.release()  # release capture, to be nice!
        self._cam = None

    def loop(self):
        """Main camera loop
        """
        self.fps.start()
        if self.console_enabled:
            self.ui.loop(self.loading, self.fps.framerate,
                         self.loadingColour, self.frameInterval)
        # Clamp frame interval
        # TODO: Refactor this into a dedicated clamp function!
        if self.frameInterval < 1:
            self.frameInterval = 1
        if self.frameInterval > 50:
            self.frameInterval = 50
        try:
            # Capture frame-by-frame
            ret, frame = self.cam.read()
            # Convert to B&W
            # and grrr val please don't go doing find and replace to fix the spelling of colour, it busts this mate.
            grayVersion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Delete the OG frame to save memory
            del frame
            preview = cv2.resize(grayVersion, (320, 180))
            self.frame = preview
            #cv2.imshow('Current loading colour {} with range {}'.format(
            #    self.loadingColour, self.colourRange), preview)
            # Advance the frame counter!
            self.frameTimer += 1
            # if it worked, we're on a working camera!!!!!
            self.finder.currentCamWorking()
        except cv2.error:
            self.frame = None
            self.ds['log'] = self.ds['log'].info('Getting new camera!')
            self.markCamAsBorked()
            return
        if self.frameTimer >= self.frameInterval:
            self.lastCheckLoad = self.loading
            self.loading = checkIfLoading(
                grayVersion, self.pixelsToSkip, self.loadingColour, self.colourRange)
        try:
            if self.loading:
                self.livesplit.pauseGameTimer()
                if not self.wasPaused:
                    self.ds['log'] = self.ds['log'].info('pausing game timer')
                    self.wasPaused = True
            else:
                self.livesplit.startGameTimer()
                if self.wasPaused:
                    self.ds['log'] = self.ds['log'].info('resuming game timer')
                    self.wasPaused = False
            if not self.ds.get('livesplit_connected'):
                self.ds['log'] = self.ds['log'].info('reconnected to livesplit!')
            self.ds['livesplit_connected'] = True
        except ConnectionRefusedError:
            if self.ds.get('livesplit_connected'):
                self.ds['log'] = self.ds['log'].warn("failed to connect to LiveSplit.server! Cannot pause - check it's running.")
                self.ds['livesplit_connected'] = False
        key = cv2.waitKey(1)
        action = self.ds.get('action')
        if action is not None:
            self.ds['log'] = self.ds['log'].info('consumed action: {}'.format(action))
            print('consumed action: {}'.format(action))
        # TODO: Replace with web commands!
        if key & 0xFF == ord('q') or action == 'quit':
            self.markCamAsBorked()
            sys.exit(0)
        if key & 0xFF == ord('d') or action == 'nextCam':
            self.finder.camDirectionForward = True
            self.markCamAsBorked()
        if key & 0xFF == ord('a') or action == 'prevCam':
            self.finder.camDirectionForward = False
            self.markCamAsBorked()
        if key & 0xFF == ord('o') or action == 'lowerInterval':
            self.frameInterval -= 1
            self.ui.forceToRender()
        if key & 0xFF == ord('p') or action == 'higherInterval':
            self.frameInterval += 1
            self.ui.forceToRender()
        if key & 0xFF == ord('b') or action == 'calibrate':
            self.loadingColour = int(grayVersion[0, 0])
            self.ui.forceToRender()
            cv2.destroyAllWindows()
        if self.lastCheckLoad != self.loading:  # SOMETHING CHANGED ! Refresh UI now.
            self.ui.forceToRender()
        self.ds['action'] = None
        self.fps.end()

def start(ds):
    print('Starting capture system...')
    cookstar = Cookstar()
    cookstar.ds = ds
    if ds.get('hide_console', False):
        cookstar.console_enabled = False
    while True:
        cookstar.loop()
        if ds.get('frameInterval'):
            cookstar.frameInterval = ds['frameInterval']
        if cookstar.frame is not None:
            ds['capturing'] = True
            ds['frame'] =  cookstar.frame
            ds['log'] = ds['log'].debug("Saved frame to shared memory")
        else:
            ds['capturing'] = False
            ds['frame'] = None
            ds['log'] = ds['log'].debug("Could not get frame to put in shared memory!")
        ds['fps'] = cookstar.fps.framerate
        ds['loading'] = cookstar.loading
        ds['frameInterval'] = cookstar.frameInterval
        ds['loadingColour'] = cookstar.loadingColour
        time.sleep(1/120)

if __name__ == '__main__':
    start(dict())
