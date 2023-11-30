import cv2
import numpy as np
import matplotlib.pyplot as plt

# hsv colors of the snooker table
lower = np.array([42, 50, 50])
upper = np.array([200, 255, 255])

def sort_ball(color, result, x, y):
  if(color[0] > 30 and color[0] < 60 and color[1] > 50 and color[1] < 80 and color[2] > 160 and color[2] < 190):
    result['red'].append({
      'x': x,
      'y': y,
    })
  if (color[0] > 180 and color[0] < 200 and color[1] > 240 and color[1] < 255 and color[2] > 240 and color[2] < 255):
    result['white'] = {
      'x': x,
      'y': y,
    }
  if (color[0] > 30 and color[0] < 50 and color[1] > 240 and color[1] < 255 and color[2] > 240 and color[2] < 255):
    result['yellow'] = {
      'x': x,
      'y': y,
    }
  if (color[0] > 150 and color[0] < 190 and color[1] > 150 and color[1] < 190 and color[2] > 40 and color[2] < 70):
    result['blue'] = {
      'x': x,
      'y': y,
    }
  if (color[0] > 10 and color[0] < 30 and color[1] > 60 and color[1] < 80 and color[2] > 10 and color[2] < 30):
    result['black'] = {
      'x': x,
      'y': y,
    }

  if (color[0] > 100 and color[0] < 130 and color[1] > 140 and color[1] < 170 and color[2] > 210 and color[2] < 255):
    result['pink'] = {
      'x': x,
      'y': y,
    }
  if (color[0] > 60 and color[0] < 90 and color[1] > 130 and color[1] < 160 and color[2] > 170 and color[2] < 200):
    result['orange'] = {
      'x': x,
      'y': y,
    }
  #green does not exist, it cannot hurt you



def draw_balls(ctrs, background, radius, result):
  size = -1
  K = np.ones((3, 3), np.uint8)

  final = background.copy()
  mask = np.zeros(background.shape[:2], np.uint8)  # empty image

  for x in range(len(ctrs)):  # for all contours

    # find center of contour
    M = cv2.moments(ctrs[x])
    cX = int(M['m10'] / M['m00'])  # X pos of contour center
    cY = int(M['m01'] / M['m00'])  # Y pos

    mask[...] = 0  # reset the mask for every ball
    cv2.drawContours(mask, ctrs, x, 255, -1)  # draws mask for each contour
    mask = cv2.erode(mask, K, iterations=3)  # erode mask several times to filter green color around balls contours


    # balls design:

    # circle to represent snooker ball
    sort_ball(cv2.mean(background, mask), result, cX, cY)
    final = cv2.circle(final,  # img to draw on
                       (cX, cY),  # position on img
                       radius,  # radius of circle - size of drawn snooker ball
                       cv2.mean(background, mask),
                       # color mean of each contour-color of each ball (src_img=transformed img)
                       size)  # -1 to fill ball with color

    # add black color around the drawn ball (for cosmetics)
    final = cv2.circle(final, (cX, cY), radius, 0, 1)

  return final


def filter_ctrs(ctrs, imw, imh, max=70, min_s=20, max_s=1000, alpha=3.445):
  filtered_ctrs = []  # list for filtered contours

  for i in range(len(ctrs)):  # for all contours

    rot_rect = cv2.minAreaRect(ctrs[i])  # area of rectangle around contour
    w = rot_rect[1][0]
    h = rot_rect[1][1]
    x, y = rot_rect[0]
    area = cv2.contourArea(ctrs[i])

    # remove from sides
    if (x < max or x > (imw - max)) or (y < max or y > (imh - max)):
      continue

    if (h * alpha < w) or (w * alpha < h):  # if the contour isnt the size of a snooker ball
      continue

    if (area < min_s) or (area > max_s):
      continue
    filtered_ctrs.append(ctrs[i])

  return filtered_ctrs


def find_balls(src, result):
  kernel = np.ones((5, 5), np.uint8)

  # apply blur
  blur_RGB = cv2.GaussianBlur(src, (5, 5), cv2.BORDER_DEFAULT)  # blur applied
  # Using cv2.erode() method
  erode = cv2.erode(blur_RGB, kernel, iterations=3)
  transformed_blur = cv2.dilate(erode, kernel, iterations=3)
  # mask
  mask_white = cv2.inRange(transformed_blur, np.array([150, 150, 150]), np.array([255, 255, 255]))
  mask_red = cv2.inRange(transformed_blur, np.array([0, 0, 100]), np.array([255, 255, 255]))
  mask_bb = cv2.inRange(transformed_blur, np.array([0, 0, 0]), np.array([70, 70, 70]))
  mask_p = cv2.inRange(transformed_blur, np.array([0, 0, 0]), np.array([255, 155, 50]))
  mask = cv2.bitwise_or(cv2.bitwise_or(cv2.bitwise_or(mask_white, mask_red), mask_bb), mask_p)

  # find contours and filter them
  ctrs, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours
  ctrs = filter_ctrs(ctrs, len(mask[0]), len(mask))  # filter contours by sizes and shapes
  # draw table+balls



  final = draw_balls(ctrs, src, 8, result)  # draw all found contours


  return final
