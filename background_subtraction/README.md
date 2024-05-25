# Background Subtraction Technique

This is the most naive approach, basically we do the following steps:
- loop over camera input
- Have a calibration phase when we get the average of the background
- We difference the background from each frame with `absdiff()`
- calculate the threshold with `threshold()` and return the contours with `getContours`
- get a slice of the image containing only the contourn with `convecHull()`
- get the center of the image and compare it to a list of centers to know if the hand is moving, do this every 8 frames
- count the number of raised finghers by intersecting a line at the top of the slice with the contourns
- if the fingher raised are one, and then we move left or right, we change desktop (TODO)

