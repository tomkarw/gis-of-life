import cv2 as cv
import numpy as np


def color_diff(c1, c2):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2) ** 0.5


def closest_color(colors, target):
    return min(colors, key=lambda c: color_diff(c, target))


def simplify_colors(bitmap, color_palette):
    simplified_image = np.zeros_like(bitmap)
    for x in range(len(bitmap)):
        for y in range(len(bitmap[x])):
            simplified_image[x][y] = closest_color(color_palette, bitmap[x][y])

    return simplified_image


def process_image(path_to_img):
    image = cv.imread(path_to_img)
    edged_image = np.zeros_like(image)

    for i in range(len(image)):
        for j in range(len(image[i])):
            if image[i][j][0] == 255 and image[i][j][1] == 0 and image[i][j][2] == 0:
                edged_image[i][j] = [255, 255, 255]
            else:
                edged_image[i][j] = [0, 0, 0]

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))
    edged_image = cv.dilate(edged_image, kernel)
    edged_image = cv.morphologyEx(edged_image, cv.MORPH_CLOSE, kernel)
    edged_image = cv.cvtColor(edged_image, cv.COLOR_BGR2GRAY)
    contours, hierarchy = cv.findContours(edged_image.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    edged_image = cv.cvtColor(edged_image, cv.COLOR_GRAY2RGB)

    for contour in contours:
        cv.drawContours(edged_image, contour, 0, (255, 0, 0), -1)

    hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    lower_blue = np.array([94, 40, 40])
    upper_blue = np.array([130, 255, 255])
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([75, 255, 255])

    res_water = cv.bitwise_and(image, image, mask=cv.inRange(hsv, lower_blue, upper_blue))
    res_grass = cv.bitwise_and(image, image, mask=cv.inRange(hsv, lower_green, upper_green))

    res = cv.bitwise_or(res_grass, res_water)
    res = cv.bitwise_or(res, edged_image)

    color_palette = [[100, 0, 0], [0, 100, 0], [0, 0, 0]]
    res = simplify_colors(res, color_palette)

    dim = (1400, 500)
    resized = cv.resize(res, dim, interpolation=cv.INTER_AREA)

    step_size = 10
    for y in range(0, resized.shape[0], step_size):
        for x in range(0, resized.shape[1], step_size):
            pixel = [0, 0, 0]
            for j in range(y, y + step_size):
                for i in range(x, x + step_size):
                    if resized[j, i, 0] == 100:
                        pixel[0] += 1
                    elif resized[j, i, 1] == 100:
                        pixel[1] += 1
                    else:
                        pixel[2] += 1

            if pixel[0] > pixel[1] and pixel[0] > pixel[2]:
                for j in range(y, y + step_size):
                    for i in range(x, x + step_size):
                        resized[j][i][0] = 100
                        resized[j][i][1] = 0
                        resized[j][i][2] = 0
            elif pixel[1] > pixel[0] and pixel[1] > pixel[2]:
                for j in range(y, y + step_size):
                    for i in range(x, x + step_size):
                        resized[j][i][0] = 0
                        resized[j][i][1] = 100
                        resized[j][i][2] = 0
            else:
                for j in range(y, y + step_size):
                    for i in range(x, x + step_size):
                        resized[j][i][0] = 0
                        resized[j][i][1] = 0
                        resized[j][i][2] = 0

    dim = (140, 50)
    final_map = cv.resize(resized, dim, interpolation=cv.INTER_AREA)

    return final_map
