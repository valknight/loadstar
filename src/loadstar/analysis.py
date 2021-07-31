from loadstar.util import BoundingBox

PRINT_FAIL_COLOUR = False


# Colours are in a range from 0 -> 255
# We're fine to look from colours 0 -> 10


def checkIfLoading(grayVersion, pixelsToSkip: int, loadingColour: int, colourRange: int, box: BoundingBox = None):
    width, height = grayVersion.shape
    if box is None:
        box = BoundingBox((0,0),(width, height))
    loading = True
    skip = False
    for x in range(0, width, pixelsToSkip):
        if skip:
            break
        for y in range(0, height, pixelsToSkip):
            if box.isInside(x,y):
                if grayVersion[x, y] > loadingColour + colourRange or grayVersion[x, y] < loadingColour - colourRange:
                    # ALL pixels must be loading for Cookstar.
                    loading = False
                    skip = True
                    if PRINT_FAIL_COLOUR:
                        print("failed to verify loading at: {} (x,y : {},{})".format(
                            grayVersion[x, y], x, y))
                    break
    return loading
