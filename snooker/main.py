import cv2
from snooker_table import find_snooker_table
from balls import find_balls
from holes import find_holes

if __name__ == '__main__':
    # Read the image
    img = cv2.imread("asd2.png")
    cv2.imshow('Original image', img)

    img, snooker_table = find_snooker_table(img)

    # Display the result
    cv2.imshow('Snooker Table', img)
    cv2.imshow('asd', find_balls(snooker_table))
    cv2.imshow('Holes', find_holes(snooker_table))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
