
PRINT_FAIL_COLOUR = False


def checkIfLoading(grayVersion, pixelsToSkip: int, loadingColour: int, colourRange: int):
    h, w = grayVersion.shape
    loading = True
    skip = False
    for x in range(0, h, pixelsToSkip):
        if skip:
            break
        for y in range(0, w, pixelsToSkip):
            if grayVersion[x, y] > loadingColour + colourRange or grayVersion[x, y] < loadingColour - colourRange:
                # ALL pixels must be loading for Cookstar.
                loading = False
                skip = True
                if PRINT_FAIL_COLOUR:
                    print("failed to verify loading at: {} (x,y : {},{})".format(
                        grayVersion[x, y], x, y))
                break
    return loading
