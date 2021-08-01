from loadstar.util import BoundingBox
from loadstar.analysis import checkIfLoading
import cv2
import click
import os

class VideoAnalyser():
    """Purpose: take mp4 file, and work out which frames are loading frames, and which are gameplay
    Spit out a NEW mp4 file, with load frames removed
    """

    def __init__(self, path: str, box: BoundingBox = None):
        """create the video analysis

        :param path: path to the mp4 file
        :type path: str
        :param box: bounding box of pixels we want to analyse. if default of none, entire frame is analysed.
        :type box: BoundingBox, optional
        """
        self.currentFrame = 1
        self.video = cv2.VideoCapture(path)
        fps = self.video.get(cv2.CAP_PROP_FPS)
        self.length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self._fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        self.writer = cv2.VideoWriter("{}-loadless.avi".format(path), cv2.VideoWriter_fourcc(*"MJPG"), fps, (640,360))
        self.loadingFrames = 0

    @property
    def nextFrame(self):
        r, frame = self.video.read()
        grayVersion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayVersion = cv2.resize(grayVersion, (1280, 720))
        self.currentFrame += 1
        return grayVersion, frame

    def checkNextFrame(self):
        frame, color = self.nextFrame
        return not(checkIfLoading(frame, 5, 0, 10, BoundingBox((100, 100), (300, 300)))), color

    def loop(self):
        if self.currentFrame >= self.length:
            self.writer.release()
            return False
        a, b = self.checkNextFrame()
        if a:
            b = cv2.resize(b, (640,360))
            self.writer.write(b.astype('uint8'))
        else:
            self.loadingFrames += 1
        return True

    def convert(self):
        hibernate = True
        if hibernate:
            print("Hibernation is on! We'll hibernate your PC once this is complete. Turn off your monitor, and go take a nap :)")
        print("Starting to convert file...")
        with click.progressbar(range(0,self.length), show_pos=True) as bar:
            for a in bar:
                bar.label = "removed {} loading frames".format(self.loadingFrames)
                v.loop()
        if hibernate:
            print("Done! Hibernating PC - see you in the morning!")
            os.system('shutdown /h')

if __name__ == '__main__':
    v = VideoAnalyser('tmp/laura.mp4')
    v.convert()