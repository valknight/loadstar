import cv2
import livesplit
import click
import sys
from loadstar.fps import FPSCounter
from loadstar.console import ConsoleUI
from loadstar.camera import CamFinder, NoMoreCamerasException
from loadstar.analysis import checkIfLoading


class Cookstar():
    def __init__(self):
        self._livesplitConnection = None
        self._cam = None
        self.fps = FPSCounter()
        self.finder = CamFinder()
        self.loading = False
        self.ui = ConsoleUI()
        self.lastCheckLoad = False

        # true black. reset this with "b" if your capture card is different.
        self.loadingColour = 0
        # allow two either side of the loadingColour (IE: if loading colour is 3, and range is 2, loading colours are defined as between 1 and 5 inclusive)
        self.colourRange = 10

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
                click.echo(
                    "No more cameras! Quitting. Check OBS VirtualCam is working right.")
                cv2.destroyAllWindows()
                sys.exit(1)
        return self._cam

    def markCamAsBorked(self):
        """Does what it says on the tin - marks the current camera in use as not working, and will cause a new camera to be found next time .cam is requested
        Can also be used if you just... want a new camera!
        """
        self.cam.release()  # release capture, to be nice!
        self._cam = None

    def loop(self):
        self.fps.start()
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
            cv2.imshow('Current loading colour {} with range {}'.format(
                self.loadingColour, self.colourRange), preview)
            # Advance the frame counter!
            self.frameTimer += 1
            # if it worked, we're on a working camera!!!!!
            self.finder.currentCamWorking()
        except cv2.error:
            print("Getting new camera!")
            self.markCamAsBorked()
            return
        if self.frameTimer >= self.frameInterval:
            self.lastCheckLoad = self.loading
            self.loading = checkIfLoading(
                grayVersion, self.pixelsToSkip, self.loadingColour, self.colourRange)
            frameTimer = 0
        if self.loading:
            self.livesplit.pauseGameTimer()
        else:
            self.livesplit.startGameTimer()
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            self.livesplit.startTimer()
        if key & 0xFF == ord('q'):
            self.markCamAsBorked()
            sys.exit(0)
        if key & 0xFF == ord('d'):
            self.finder.camDirectionForward = True
            self.markCamAsBorked()
        if key & 0xFF == ord('a'):
            self.finder.camDirectionForward = False
            self.markCamAsBorked()
        if key & 0xFF == ord('o'):
            self.frameInterval -= 1
            self.ui.forceToRender()
        if key & 0xFF == ord('p'):
            self.frameInterval += 1
            self.ui.forceToRender()
        if key & 0xFF == ord('b'):
            self.loadingColour = int(grayVersion[0, 0])
            self.ui.forceToRender()
            cv2.destroyAllWindows()
        if self.lastCheckLoad != self.loading:  # SOMETHING CHANGED ! Refresh UI now.
            self.ui.forceToRender()
        self.fps.end()


if __name__ == '__main__':
    cookstar = Cookstar()
    while True:
        cookstar.loop()
