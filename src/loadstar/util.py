class BoundingBox():
    def __init__(self, topLeft: tuple, bottomRight: tuple) -> None:
        self.topLeft = topLeft
        self.bottomRight = bottomRight

    def isInside(self, x:int, y:int, p=True):
        if self.topLeft[0] <= x and self.bottomRight[0] >= x:
            if self.topLeft[1] <= y and self.bottomRight[1] >= y:
                return True
        return False