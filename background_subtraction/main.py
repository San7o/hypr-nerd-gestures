import cv2
import numpy as np

from HandData import HandData
from helpers import *
from Config import Config

def main():

    # Setting up variables
    conf = Config.default()

    # Readming camera input
    capture = cv2.VideoCapture(0)

    # Main loop
    while (True):
        # Store the frame from the video capture and resize it
        # to the desired window size.
        ret, frame = capture.read()
        frame = cv2.resize(frame, (conf.FRAME_WIDTH, conf.FRAME_HEIGHT))

        # Flip the frame over the vertical axis so that it
        # works like a mirror, which is more intuitive to the user.
        frame = cv2.flip(frame, 1)

        # Separate the region of interest and prep it for edge detection.
        region = get_region(frame, conf)

        if conf.frames_elapsed < conf.CALIBRATION_TIME:
            conf = get_average(region, conf)
        # Recalibrate the background
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            conf.frames_elapsed = 0
        else:
            (conf.hand, region_pair) = segment(region, conf)
            if region_pair is not None:
                # If we have the regions segmented successfully,
                # show them in another window for the user.
                (thresholded_region, segmented_region) = region_pair
                cv2.drawContours(region, [segmented_region], -1, (255, 255, 255))
                cv2.imshow("Segmented Image", region)
                
                conf.hand = get_hand_data(thresholded_region, segmented_region, conf)

        # Write the action the hand is doing on the screen,
        # and draw the region of interest.
        write_on_image(frame, conf)
        
        cv2.imshow("Camera Input", frame)
        conf.frames_elapsed += 1

        # Check if user wants to exit.
        if (cv2.waitKey(1) & 0xFF == ord('x')):
            break

    # When we exit the loop, we have to stop the capture too.
    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
