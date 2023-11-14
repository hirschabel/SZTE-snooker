import cv2
from snooker_table import find_snooker_table
from balls import find_balls
from holes import find_holes

if __name__ == '__main__':
    # Read the image
    orig_image = cv2.imread("videos/bemutato.png")

    # Find snooker table boundaries
    img, snooker_table = find_snooker_table(orig_image.copy())

    # Find balls present on table
    balls = find_balls(snooker_table.copy())

    # Find holes
    holes = find_holes(snooker_table.copy())

    # Final image
    final_image = cv2.addWeighted(balls, 0.5, holes, 0.5, 0)

    # ======Results======
    # Original Image
    cv2.imshow('Original Image', orig_image)
    cv2.waitKey(0)

    # Snooker Table
    cv2.imshow('Snooker Table', snooker_table)
    cv2.waitKey(0)

    # Balls Highlighted
    cv2.imshow('Balls Highlighted', balls)
    cv2.waitKey(0)

    # Holes Highlighted
    cv2.imshow('Holes Highlighted', holes)
    cv2.waitKey(0)

    # Final image
    cv2.imshow('Final', final_image)
    cv2.waitKey(0)

    # Clean-up
    cv2.destroyAllWindows()
