import cv2
import numpy as np
import matplotlib.pyplot as plt

# hsv colors of the snooker table
lower = np.array([42, 50, 50])
upper = np.array([200, 255, 255])

def draw_balls(ctrs, background, radius=7, size=-1, img=0):
    K = np.ones((3, 3), np.uint8)

    final = background.copy()
    height, width, channels = img.shape
    mask = np.zeros((width, height, channels), np.uint8)  # empty image

    for x in range(len(ctrs)):  # for all contours

        # find center of contour
        M = cv2.moments(ctrs[x])
        cX = int(M['m10'] / M['m00'])  # X pos of contour center
        cY = int(M['m01'] / M['m00'])  # Y pos

        mask[...] = 0  # reset the mask for every ball
        cv2.drawContours(mask, ctrs, x, 255, -1)  # draws mask for each contour
        mask = cv2.erode(mask, K, iterations=3)  # erode mask several times to filter green color around balls contours



        # add black color around the drawn ball (for cosmetics)
        final = cv2.circle(final, (cX, cY), radius, 0, 3)

        # small circle for light reflection
        final = cv2.circle(final, (cX - 2, cY - 2), 2, (255, 255, 255), -1)

    return final


def filter_ctrs(ctrs, imw, imh, max=50, min_s=5, max_s=1000, alpha=3.445):
    filtered_ctrs = []  # list for filtered contours


    for i in range(len(ctrs)):  # for all contours

        rot_rect = cv2.minAreaRect(ctrs[i])  # area of rectangle around contour
        w = rot_rect[1][0]
        h = rot_rect[1][1]
        x, y = rot_rect[0]
        area = cv2.contourArea(ctrs[i])

        #remove from sides
        #print(x)
        #print(y)
        #print(imw - max)
        #print('---')
        if (x < max or x > (imw - max)) or (y < max or y > (imh - max)):
            continue

        if (h * alpha < w) or (w * alpha < h):  # if the contour isnt the size of a snooker ball
            continue

        if (area < min_s) or (area > max_s):
            continue
        filtered_ctrs.append(ctrs[i])

    return filtered_ctrs

def find_balls(src):


    # apply blur
    transformed_blur = cv2.GaussianBlur(src, (11, 11), cv2.BORDER_DEFAULT)  # blur applied
    blur_GRAY = cv2.cvtColor(transformed_blur, cv2.COLOR_BGR2GRAY)  # rgb version
    # mask
    mask = cv2.inRange(blur_GRAY, 40, 120)  # table's mask
    #cv2.imshow('asd Table', mask)

    # find contours and filter them
    ctrs, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
    #print(len(mask))
    #print(len(mask[0]))
    ctrs = filter_ctrs(ctrs, len(mask[0]), len(mask))  # filter contours by sizes and shapes
    # draw table+balls
    final = draw_balls(ctrs, src, radius=8, img=src)  # draw all found contours

    return final
