import cv2
import numpy as np

from HandData import HandData
from Config import Config
from HandData import Waving

# Here we take the current frame, the number of frames
# elapsed, and how many fingers we've detected
# so we can print on the screen which gesture is happening
# (or if the camera is calibrating).
def write_on_image(frame, conf):

    hand = conf.hand

    text = "Searching..."

    if conf.frames_elapsed < conf.CALIBRATION_TIME:
        text = "Calibrating..."
    elif hand == None or hand.isInFrame == False:
        text = "No hand detected"
    else:
        if hand.Waving is Waving.LEFT:
            text = "Waving Left"
        elif hand.Waving is Waving.RIGHT:
            text = "Waving Right"
        elif hand.fingers == 0:
            text = "Rock"
        elif hand.fingers == 1:
            text = "Pointing"
        elif hand.fingers == 2:
            text = "Scissors"
    
    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX,
                0.4,( 0 , 0 , 0 ),2,cv2.LINE_AA)
    cv2.putText(frame, text, (10,20), cv2.FONT_HERSHEY_COMPLEX,
                0.4,(255,255,255),1,cv2.LINE_AA)

    # Highlight the region of interest using a drawn rectangle.
    cv2.rectangle(frame, (conf.region_left, conf.region_top),
                  (conf.region_right, conf.region_bottom), (255,255,255), 2)


# This function captures the background
def get_region(frame, conf):

    # Separate the region of interest from the rest of the frame.
    region = frame[conf.region_top:conf.region_bottom,
                   conf.region_left:conf.region_right]
    # Make it grayscale so we can detect the edges more easily.
    region = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    # Use a Gaussian blur to prevent frame noise from being labeled as an edge.
    region = cv2.GaussianBlur(region, (5,5), 0)

    return region


# This function captures the background
def get_average(region, conf):

    # If we haven't captured the background yet, make the current region the background.
    if conf.background is None:
        conf.background = region.copy().astype("float")
        return conf
    # Otherwise, add this captured frame to the average of the backgrounds.
    cv2.accumulateWeighted(region, conf.background, conf.BG_WEIGHT)

    return conf


# Here we use differencing to separate the
# background from the object of interest.
def segment(region, conf):

    # Find the absolute difference between the
    # background and the current frame.
    diff = cv2.absdiff(conf.background.astype(np.uint8),
                       region)

    # Threshold that region with a strict 0 or 1
    # ruling so only the foreground remains.
    thresholded_region = cv2.threshold(diff, conf.OBJ_THRESHOLD,
                                       255, cv2.THRESH_BINARY)[1]

    # Get the contours of the region, which will
    # return an outline of the hand.
    (contours, _) = cv2.findContours(thresholded_region.copy(),
                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If we didn't get anything, there's no hand.
    if len(contours) == 0:
        if conf.hand is not None:
            conf.hand.isInFrame = False
        return (conf.hand, None)
    # Otherwise return a tuple of the filled hand
    # (thresholded_region), along with the outline (segmented_region).
    else:
        if conf.hand is not None:
            conf.hand.isInFrame = True
        segmented_region = max(contours, key = cv2.contourArea)
        return (conf.hand, (thresholded_region, segmented_region))



# This function gets the hand data from the segmented image.
def get_hand_data(thresholded_image, segmented_image, conf):

    hand = conf.hand

    # Enclose the area around the extremities in a convex hull to connect all outcroppings.
    convexHull = cv2.convexHull(segmented_image)
    
    # Find the extremities for the convex hull and store them as points.
    top    = tuple(convexHull[convexHull[:, :, 1].argmin()][0])
    bottom = tuple(convexHull[convexHull[:, :, 1].argmax()][0])
    left   = tuple(convexHull[convexHull[:, :, 0].argmin()][0])
    right  = tuple(convexHull[convexHull[:, :, 0].argmax()][0])
    
    # Get the center of the palm, so we can check for waving and find the fingers.
    centerX = int((left[0] + right[0]) / 2)

    # We put all the info into an object for handy extraction (get it? HANDy?)
    if hand == None:
        hand = HandData(top, bottom, left, right, centerX)
    else:
        hand.update(top, bottom, left, right)
    
    # Wait 8 frames
    if conf.frames_elapsed % 6 == 0:
        hand.check_for_waving(centerX)

    # We count the number of fingers up every frame,
    # but only change hand.fingers if
    # 12 frames have passed, to prevent erratic gesture counts.
    hand.gestureList.append(count_fingers(thresholded_image, conf))
    if conf.frames_elapsed % 8 == 0:
        hand.fingers = most_frequent(hand.gestureList)
        hand.gestureList.clear()

    return hand

# This function counts the number of fingers
def count_fingers(thresholded_image, conf):
    
    hand = conf.hand
    if hand == None:
        return

    # Find the height at which we
    # will draw the line to count fingers.
    line_height = int(hand.top[1] +
                      (0.2 * (hand.bottom[1] - hand.top[1])))
    
    # Get the linear region of interest
    # along where the fingers would be.
    line = np.zeros(thresholded_image.shape[:2], dtype=np.uint8)
    
    # Draw a line across this region of interest.
    cv2.line(line, (thresholded_image.shape[1], line_height), (0, line_height), 255, 1)
    
    # Do a bitwise AND to find where the line
    # intersected the hand -- this is where the fingers are!
    line = cv2.bitwise_and(thresholded_image,
                           thresholded_image, mask = line.astype(np.uint8))
    
    # Get the line's new contours. The contours are
    # basically just little lines formed by gaps 
    # in the big line across the fingers, so each would
    # be a finger unless it's very wide.
    (contours, _) = cv2.findContours(line.copy(),
                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    fingers = 0
    
    # Count the fingers by making sure the contour lines
    # are "finger-sized", i.e. not too wide.
    # This prevents a "rock" gesture from being mistaken for a finger.
    for curr in contours:
        width = len(curr)
        
        if width < 3 * abs(hand.right[0] - hand.left[0]) / 4 and width > 5:
            fingers += 1
    
    return fingers


# This function finds the most frequent element in a list.
def most_frequent(input_list):
    dict = {}
    count = 0
    most_freq = 0
    
    for item in reversed(input_list):
        dict[item] = dict.get(item, 0) + 1
        if dict[item] >= count :
            count, most_freq = dict[item], item
    
    return most_freq
