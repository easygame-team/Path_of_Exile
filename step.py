from time import sleep
from move_window_left import run
from random import randint
from mss import mss
import pyautogui
import numpy as np
import cv2.cv2 as cv2


def find_white(original_image):
    image_str = np.asarray(original_image)
    gray = cv2.cvtColor(image_str, cv2.COLOR_BGR2GRAY)
    ret, threshold1 = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 1))
    closed = cv2.morphologyEx(threshold1, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, kernel, iterations=1)
    closed = cv2.dilate(closed, kernel, iterations=1)
    return closed


frame= {'top': 92, 'left': 440, 'width': 80, 'height': 18}
sct = mss()


def  movement_of_the_player():
    while True:
        x = randint(300, 836)
        y = randint(80, 450)
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click(x, y, duration=0.2)


def entry():
    run()
    sleep(5)
    pyautogui.click(648,468,duration=0.2)
    pyautogui.click(648,468,duration=0.2)
    sleep(5)
    pyautogui.click(810,433,duration=0.2)
    pyautogui.click(810,433,duration=0.2)


def main():
    entry()
    movement_of_the_player()



if __name__ == '__main__':
    main()