from cv2 import imread, cvtColor, IMREAD_UNCHANGED, COLOR_BGRA2RGB

class Needle:
    # properties
    name = ""
    img = None
    transparent = False
    mask = None
    width = 0
    height = 0
    last_location = None

    # constructor
    def __init__(self, img_path, transparent=False):
        self.img_path = "scripts/images/" + img_path
        self.name = img_path
        img = imread(self.img_path, IMREAD_UNCHANGED)
        if transparent == True:
            self.transparent = True
            self.mask = img[:, :, 3]
        self.width = img.shape[1]
        self.height = img.shape[0]
        self.img = cvtColor(img, COLOR_BGRA2RGB)