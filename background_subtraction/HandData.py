from enum import Enum
from hyprland import *

class Waving(Enum):
    LEFT = 0
    RIGHT = 1
    NONE = 2

# Data structure for storing hand data
class HandData:
    top = (0,0)
    bottom = (0,0)
    left = (0,0)
    right = (0,0)
    centerX = 0
    prevCenterX = 0
    isInFrame = False
    Waving = Waving.NONE
    fingers = 0
    gestureList = []
    
    def __init__(self, top, bottom,
                 left, right, centerX):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.centerX = centerX
        self.prevCenterX = 0
        self.isInFrame = False
        self.Waving = Waving.NONE
        
    def update(self, top, bottom,
               left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def check_for_waving(self, centerX):
        self.prevCenterX = self.centerX
        self.centerX = centerX
        
        if abs(self.centerX - self.prevCenterX) > 10:
            if self.centerX > self.prevCenterX:

                #if self.fingers == 1: # Pointing
                move_workspace_right()

                self.Waving = Waving.RIGHT
            else:

                #if self.fingers == 1:
                move_workspace_left()

                self.Waving = Waving.LEFT
        else:
            self.Waving = Waving.NONE

        print(self.isInFrame)
