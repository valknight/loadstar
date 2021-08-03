class CoordinateError(Exception):
    pass

class BoundingBox():
    def __init__(self, topLeft: tuple, bottomRight: tuple) -> None:
        if topLeft[0] > bottomRight[0]:
            raise CoordinateError('minx cannot be larger than maxx')
        if topLeft[1] > bottomRight[1]:
            raise CoordinateError('minx cannot be larger than maxx')
        self.topLeft = topLeft
        self.bottomRight = bottomRight

    def isInside(self, x:int, y:int, p=True):
        if self.topLeft[0] <= x and self.bottomRight[0] >= x:
            if self.topLeft[1] <= y and self.bottomRight[1] >= y:
                return True
        return False