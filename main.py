from skimage import io, color
import numpy as np
import random
import math
import time
import sys
import cv2

def distance(lab1, lab2):
    delta = abs(lab1[0] - lab2[0]) ** 2 + abs(lab1[1] - lab2[1]) ** 2 + abs(lab1[2] - lab2[2]) ** 2
    return delta

def get_webcam():
    _, frame = cap.read()

    w = len(frame[0])
    h = len(frame)

    w2 = 238
    ratio = w2 / w
    h2 = (int)(ratio * h)

    frame = cv2.resize(frame, (w2, h2))

    for x in range(len(frame)):
        for y in range(len(frame[x])):
            tmp = frame[x][y][0]
            frame[x][y][0] = frame[x][y][2]
            frame[x][y][2] = tmp
    return frame

def print_img(img):
    img_lab = color.rgb2lab(img)

    blocks_rgb = []

    for r in (0, 95, 135, 175, 215, 255):
        for g in (0, 95, 135, 175, 215, 255):
            for b in (0, 95, 135, 175, 215, 255):
                blocks_rgb.append([r / 255, g / 255, b / 255])

    blocks_lab = color.rgb2lab([blocks_rgb])[0]

    for x in range(len(img_lab)):
        if x % 2 == 0:
            continue
        for y in range(len(img_lab[x])):
            nearest = -1
            delta = -1
            for idx, block in enumerate(blocks_lab):
                d = distance(block, img_lab[x][y])
                if d < delta or delta == -1:
                    delta = d
                    nearest = idx
            print("\033[38;5;%dm/" % (16 + nearest), end="")
        print("\033[0m")

def print_img_rnd(img):
    img_lab = color.rgb2lab(img)

    blocks_rgb = []

    for r in (0, 95, 135, 175, 215, 255):
        for g in (0, 95, 135, 175, 215, 255):
            for b in (0, 95, 135, 175, 215, 255):
                blocks_rgb.append([r / 255, g / 255, b / 255])

    blocks_lab = color.rgb2lab([blocks_rgb])[0]

    coords = [(x,y) for x in range(len(img_lab)) for y in range(len(img_lab[0]))]
    random.shuffle(coords)

    i = 0
    for y, x in coords:
        if y % 2 == 0:
            continue
        nearest = -1
        delta = -1
        for idx, block in enumerate(blocks_lab):
            d = distance(block, img_lab[y][x])
            if d < delta or delta == -1:
                delta = d
                nearest = idx
        print("\033[%d;%dH\033[38;5;%dm/" % ((int)((y+1)/2), x+1, 16 + nearest), end="")
        if i >= 300:
            sys.stdout.flush()
            i = 0
        else:
            i += 1
    print("\033[%d;1H" % len(img_lab), end="")


if len(sys.argv) > 1:
    img_rgb = io.imread(sys.argv[1])
    if len(img_rgb[0][0]) == 4:
        img_rgb = color.rgba2rgb(img_rgb)
else:
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    
    img_rgb = get_webcam()

for i in range(0, 10):
    print("\033[1;1H", end="")
    if i == 0:
        print_img(img_rgb)
    else:
        print_img_rnd(img_rgb)
    img_rgb = get_webcam()

cap.release()
