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


def process_image(path_to_img, map_width, map_height):
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

    dim = (map_width, map_height)
    resized = cv.resize(res, dim, interpolation=cv.INTER_AREA)

    for y in range(0, resized.shape[0]):
        for x in range(0, resized.shape[1]):
            pixel = [0, 0, 0]
            if resized[y, x, 0] == 100:
                pixel[0] += 1
            elif resized[y, x, 1] == 100:
                pixel[1] += 1
            else:
                pixel[2] += 1

            if pixel[0] > pixel[1] and pixel[0] > pixel[2]:
                resized[y][x] = 1
            elif pixel[1] > pixel[0] and pixel[1] > pixel[2]:
                resized[y][x] = -1
            else:
                resized[y][x] = 0.5

    return resized[:, :, 0]
