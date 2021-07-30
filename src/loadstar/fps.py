import time


class FrameTime():
    def __init__(self) -> None:
        self.startTime = time.time()
        self.endTime = None

    def finishFrame(self):
        self.endTime = time.time()

    @property
    def frameTime(self) -> float:
        return self.endTime - self.startTime


class FPSCounter():
    def __init__(self) -> None:
        self.frames = []

    def cleanup(self):
        for f in self.frames:
            if f.toDestroy():
                self.frames.remove(f)

    def start(self):
        self.frames = self.frames[-30:]
        self.frames.append(FrameTime())

    def end(self) -> int:
        self.frames[len(self.frames) - 1].finishFrame()

    @property
    def averageFrameTime(self):
        sum = 0
        for f in self.frames:
            if f.endTime:
                # we'll clean these up anyway, but, this is to ensure we don't count frames which haven't finished.
                sum += f.frameTime
        return sum / len(self.frames)

    @property
    def framerate(self):
        try:
            return round(1 / self.averageFrameTime)
        except ZeroDivisionError:
            return 0

    def getFPS(self):
        return int(self.framerate)
