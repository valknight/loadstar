import cv2


class NoMoreCamerasException(Exception):
    pass


class CamFinder:
    def __init__(self, camIndex=0) -> None:
        self.camIndex = camIndex
        self.maxCams = 50
        self.camDirectionForward = True
        self.maxBackFound = False
        self.maxForwardFound = False

    def findNewCam(self) -> None:
        if self.maxBackFound and self.maxForwardFound:
            raise NoMoreCamerasException(
                "Exhausted camera from IDs -{} to {} - check you OBS virtual cam installed and working.".format(self.maxCams, self.maxCams))
        if not self.maxForwardFound:
            self.increase_camIndex()
        else:
            # Means we have exhausted all forward, but not all back. let's go that way!
            self.reduce_camIndex()

    def currentCamWorking(self) -> None:
        self.maxBackFound = False
        self.maxForwardFound = False
        pass

    def increase_camIndex(self):
        if self.camIndex >= self.maxCams:
            self.camDirectionForward = False
            self.maxForwardFound = True
        else:
            self.camIndex += 1

    def reduce_camIndex(self):
        if self.camIndex <= - self.maxCams:
            self.camDirectionForward = True
            self.maxBackFound = True
        else:
            self.camIndex -= 1

    @property
    def cam(self) -> cv2.VideoCapture:
        self.findNewCam()
        c = cv2.VideoCapture(self.camIndex)
        c.set(3, 1280)
        c.set(4, 720)
        return c
