import cv2
import numpy as np


def find_largest_inner_circle2(contour, image_shape):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

    dist_transform = cv2.distanceTransform(mask, cv2.DIST_L2, 3)
    max_dist = np.amax(dist_transform)

    # Find the maximum distance and its location
    max_radius_loc = np.unravel_index(np.argmax(dist_transform), dist_transform.shape)
    largest_circle_center = (max_radius_loc[1], max_radius_loc[0])
    largest_radius = int(max_dist)

    return largest_circle_center, largest_radius


# Ez itt arra van, ha mondjuk valami takarja a lyukat, akkor javít a felismerésen
def find_biggest_hole2(img):
    # Kép beolvasás
    image = img

    # Szürkeárnyalat
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Fehér ÉS Feket színek elkülönítése bináris képbe (fekete+fehér/minden más)
    ret, mask_white = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Morfológiai szűrések
    kernel = np.ones((5, 5), np.uint8)
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)
    mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_CLOSE, kernel)

    # Kontúrok keresése
    contours, _ = cv2.findContours(mask_white, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Kép felső és alsó határ pixelei, amikben keressük a lyukakat
    min_x, max_x = 10, image.shape[0] - 50  # TODO: képmérethez % VAGY azonos magas képek

    biggset_contour_area = contours[0]

    for contour in contours:
        if cv2.contourArea(contour) > cv2.contourArea(biggset_contour_area):
            biggset_contour_area = contour

    x, y, w, h = cv2.boundingRect(biggset_contour_area)

    if min_x > y or y > max_x:  # x és y cserélődik, mert python :)
        largest_circle_center, largest_radius = find_largest_inner_circle2(contour, image.shape)
        if largest_circle_center is not None:
            cv2.circle(img, largest_circle_center, largest_radius, (0, 0, 255), 2)


def find_biggest_hole(img):
    # Kép beolvasás
    image = img

    # Szürkeárnyalat
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Fehér ÉS Feket színek elkülönítése bináris képbe (fekete+fehér/minden más)
    ret, mask_white = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    ret, mask_black = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)

    # Fekete és fehér maszkok uniója
    combined_mask = cv2.bitwise_or(mask_white, mask_black)

    # Morfológiai szűrések
    kernel = np.ones((5, 5), np.uint8)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    combined_mask = cv2.morphologyEx(combined_mask, cv2.MORPH_CLOSE, kernel)

    # Kontúrok keresése
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Kép felső és alsó határ pixelei, amikben keressük a lyukakat
    min_x, max_x = 10, image.shape[0] - 50

    biggset_contour_area = contours[0]

    for contour in contours:
        if cv2.contourArea(contour) > cv2.contourArea(biggset_contour_area):
            biggset_contour_area = contour

    x, y, w, h = cv2.boundingRect(biggset_contour_area)

    if min_x > y or y > max_x:  # x és y cserélődik, mert python :)
        (cx, cy), radius = cv2.minEnclosingCircle(biggset_contour_area)
        center = (int(cx), int(cy))
        radius = int(radius)

        cv2.circle(image, center, radius, (0, 0, 255), 2)


def find_holes(img, balls_in_pocket):
    # Kép beolvasás
    image = img

    # Get image dimensions
    height, width, _ = image.shape

    # Define percentages to split the image
    upper_split = 20.0  # Split for upper part (20.0%)
    lower_split = 80.0  # Split for lower part (80.0%)
    left_column_split = 33.3  # Split for left column (33.3%)
    right_column_split = 66.6  # Split for right column (66.6%)

    # Calculate splitting positions based on percentages
    upper_divider = int(height * (upper_split / 100))
    lower_divider = int(height * (lower_split / 100))
    left_column_divider = int(width * (left_column_split / 100))
    right_column_divider = int(width * (right_column_split / 100))

    # Extract regions - top and bottom rectangles excluding the middle part
    top_left_rectangle = image[:upper_divider, :left_column_divider]
    top_middle_rectangle = image[:upper_divider, left_column_divider:right_column_divider]
    top_right_rectangle = image[:upper_divider, right_column_divider:]

    bottom_left_rectangle = image[lower_divider:, :left_column_divider]
    bottom_middle_rectangle = image[lower_divider:, left_column_divider:right_column_divider]
    bottom_right_rectangle = image[lower_divider:, right_column_divider:]

    find_biggest_hole(top_left_rectangle)
    find_biggest_hole(top_middle_rectangle)
    find_biggest_hole2(top_right_rectangle) # a példán takarásban van a lyuk
    find_biggest_hole(bottom_left_rectangle)
    find_biggest_hole(bottom_middle_rectangle)
    find_biggest_hole(bottom_right_rectangle)

    # List of balls fallen in a specific pocket
    for pocket_list in balls_in_pocket:
        text = ','.join(balls_in_pocket[pocket_list])
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.8
        font_thickness = 1

        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)

        text_x = 0
        text_y = 0
        if pocket_list == "top_left":
            text_x = int(image.shape[1] * 0.05)  # 5% of the image width from the left side
            text_y = text_size[1] + 5  # 5 pixels below the top edge
        elif pocket_list == "top_middle":
            text_x = int(image.shape[1] * 0.4)  # 40% of the image width from the left side
            text_y = text_size[1] + 5  # 5 pixels below the top edge
        elif pocket_list == "top_right":
            text_x = int(image.shape[1] * 0.7)  # 70% of the image width from the left side
            text_y = text_size[1] + 5  # 5 pixels below the top edge
        elif pocket_list == "bottom_left":
            text_x = int(image.shape[1] * 0.05)  # 5% of the image width from the left side
            text_y = image.shape[0] - text_size[1] - 5  # 5 pixels above the bottom edge
        elif pocket_list == "bottom_middle":
            text_x = int(image.shape[1] * 0.4)  # 40% of the image width from the left side
            text_y = image.shape[0] - text_size[1] - 5  # 5 pixels above the bottom edge
        elif pocket_list == "bottom_right":
            text_x = int(image.shape[1] * 0.7)  # 70% of the image width from the left side
            text_y = image.shape[0] - text_size[1] - 5  # 5 pixels above the bottom edge

        cv2.putText(image, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness)


    # Draw dividing lines on the image
    cv2.line(image, (0, upper_divider), (width, upper_divider), (0, 255, 0), 2)  # Upper divider
    cv2.line(image, (0, lower_divider), (width, lower_divider), (0, 255, 0), 2)  # Lower divider
    cv2.line(image, (left_column_divider, 0), (left_column_divider, height), (0, 255, 0), 2)  # Left column divider
    cv2.line(image, (right_column_divider, 0), (right_column_divider, height), (0, 255, 0), 2)  # Right column divider

    return image
