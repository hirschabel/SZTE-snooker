import cv2
from snooker_table import find_snooker_table

if __name__ == '__main__':
    # Read the image
    img = cv2.imread("videos/3.jpg")
    cv2.imshow('Original image', img)

    img, snooker_table = find_snooker_table(img)

    # Display the result
    cv2.imshow('Snooker Table', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
