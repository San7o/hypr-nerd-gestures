
# We will use this class to store all the variables
# that we need to keep track of in one place.
class Config:

    '''
    # Hold the banground frame for background subtraction
    background = None

    # Hold the hand's data so all its details are in one place.
    hand = None


    # Variables to count how many frames have passed
    # and to set the size of the window.
    frames_elapsed = 0
    # My webcam is 4:3
    FRAME_HEIGHT = 320
    FRAME_WIDTH = 640


    # Humans come in a ton of beautiful shades and colors.
    # Try editing these if your program has trouble
    # recognizing your skin tone.
    CALIBRATION_TIME = 30
    BG_WEIGHT = 0.5
    OBJ_THRESHOLD = 18


    # Our region of interest will be the top
    # right part of the frame.
    region_top = 0
    region_bottom = int(2 * FRAME_HEIGHT / 3)
    region_left = int(FRAME_WIDTH / 2)
    region_right = 0

    frames_elapsed = 0
    '''

    # Constructor
    def __init__(self, background, hand, frames_elapsed,
                 FRAME_HEIGHT, FRAME_WIDTH, CALIBRATION_TIME,
                 BG_WEIGHT, OBJ_THRESHOLD, region_top,
                 region_bottom, region_left, region_right):

        self.background = background
        self.hand = hand
        self.frames_elapsed = frames_elapsed
        self.FRAME_HEIGHT = FRAME_HEIGHT
        self.FRAME_WIDTH = FRAME_WIDTH
        self.CALIBRATION_TIME = CALIBRATION_TIME
        self.BG_WEIGHT = BG_WEIGHT
        self.OBJ_THRESHOLD = OBJ_THRESHOLD
        self.region_top = region_top
        self.region_bottom = region_bottom
        self.region_left = region_left
        self.region_right = region_right

    # Default values
    @staticmethod
    def default():
        return Config(None, None, 0, 480, 640, 30, 0.5,
                      18, 0, 320, 0, 150)
