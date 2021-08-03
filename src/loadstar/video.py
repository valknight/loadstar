from loadstar.util import BoundingBox
from loadstar.analysis import checkIfLoading
import cv2
import click
import os
import sys

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
        self._fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        self.filename = "{}-loadless.mp4".format(path)
        self.writer = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*"MJPG"), fps, (640,360))
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
        print("Starting to convert file...")
        with click.progressbar(range(0,self.length), show_pos=True) as bar:
            for a in bar:
                bar.label = "removed {} loading frames".format(self.loadingFrames)
                self.loop()
        click.echo('Success! Check file at {}-loadless.mp4 :)'.format(self.filename))
        click.echo('If you want to avoid this in future, considering setting up LoadStar with a live video input - we integrate with LiveSplit!')

def resetToMax(v, min: int, max: int, message: str, reset: int):
    if v <= min or v >= max:
        click.echo(message, color='red')
        click.echo(message='Resetting to {}'.format(reset), color='red')
        v = reset
    return reset

def getLarger(x, y):
    if x >= y:
        return x
    return y

@click.command()
@click.option('--path', prompt='Path to file to remove loads from:', help='Path to the Cookstar VOD to remove loads from')
@click.option('--minX', default=0, help='left most X boundary you want to scan pixels from. measured from 0 -> 1280 (input frames will be resized)')
@click.option('--maxX', default=1280, help='right most X boundary you want to scan pixels up to measured from 0 -> 1280 (input frames will be resized)')
@click.option('--minY', default=0, help='The top most y boundary you wish to scan pixels from measured from 0 -> 720 (input frames will be resized)')
@click.option('--maxY', default=0, help='The bottom most y boundary you wish to scan pixels up to measured from 0 -> 720 (input frames will be resized)')
def startScan(path: str, minx: int, maxx: int, miny: int, maxy: int):
    minX = resetToMax(minx, 0, 1280, "minX must be between 0 and 1280", 0)
    maxX = resetToMax(maxx, 0, 1280, "maxX must be between 0 and 1280", 1280)
    minY = resetToMax(miny, 0, 720, "minY must be between 0 and 1280", 0)
    maxY = resetToMax(maxy, 0, 720, "maxY must be between 0 and 1280", 720)
    print(path)
    if getLarger(minX, maxX) == minX:
        click.echo("minX must be smalelr than maxX")
        sys.exit(1)
    if getLarger(minY, maxY) == minY:
        click.echo("minY must be smalelr than maxY")
        sys.exit(1)
    if not(os.path.exists(path)):
        click.echo("Please ensure the file exists at path {}".format(path))
        sys.exit(1)
    b = BoundingBox((minX, minY),(maxX, maxY))
    v = VideoAnalyser(path, box=b)
    v.convert()

if __name__ == '__main__':
    startScan()