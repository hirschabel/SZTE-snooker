import cv2
import numpy as np

def find_holes(img):
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

    # Minimum kontúr terület
    min_contour_area = 50

    # Kép felső és alsó határ pixelei, amikben keressük a lyukakat
    min_x, max_x = 10, image.shape[0] - 50  # TODO: képmérethez % VAGY azonos magas képek

    # Lyukak karikázása
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            x, y, w, h = cv2.boundingRect(contour)

            if min_x > y or y > max_x:  # x és y cserélődik, mert python :)
                (cx, cy), radius = cv2.minEnclosingCircle(contour)
                center = (int(cx), int(cy))
                radius = int(radius)

                cv2.circle(image, center, radius, (0, 0, 255), 2)

    return image
