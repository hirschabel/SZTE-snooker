import cv2
import numpy as np


def find_snooker_table(img):
    img_copy = img

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)

    # Define range of light green color in HSV
    lower_light_green = np.array([30, 100, 100])
    upper_light_green = np.array([90, 255, 255])

    # Define range of dark green color in HSV
    lower_dark_green = np.array([70, 100, 100])
    upper_dark_green = np.array([110, 255, 255])

    # Threshold the HSV image to get only light and dark green colors
    mask_light_green = cv2.inRange(hsv, lower_light_green, upper_light_green)
    mask_dark_green = cv2.inRange(hsv, lower_dark_green, upper_dark_green)

    # Combine the two masks
    mask = cv2.bitwise_or(mask_light_green, mask_dark_green)

    # Find the largest contour in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle for the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Draw the rectangle on the original image
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return img, img_copy[y:y + h, x:x + w]
