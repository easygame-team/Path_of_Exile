from time import sleep
from move_window_left import run
from mss import mss
from PIL import Image
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


frame = {'top': 92, 'left': 440, 'width': 80, 'height': 18}
sct = mss()

def screen_record():
    while (True):
        sct.get_pixels(frame)
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
        new_screen = find_white(img)
        winname = "Test"
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 1450, 100)
        cv2.imshow(winname,new_screen)
        n_white_pix = np.sum(new_screen == 255)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
        return n_white_pix

def  movement_of_the_player():
    while True:
        pix = screen_record()
        if pix>10:
            pyautogui.press('q')



def entry():
    run()
    sleep(5)
    pyautogui.click(648,468,duration=0.2)
    pyautogui.click(648,468,duration=0.2)
    sleep(10)
    pyautogui.click(810,433,duration=0.2)
    pyautogui.click(810,433,duration=0.2)

def main():
    entry()
    movement_of_the_player()

if __name__ == '__main__':
    main()