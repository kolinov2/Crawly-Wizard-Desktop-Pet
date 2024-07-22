# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#             Wizard Gnome Desktop Pet
#                    by kolino
#         Warning! this code is low effort :)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import cv2
import numpy as np
import pygame
import win32api
import win32con
import win32gui
import random
import time
import datetime

# -=-=-=-=-=-=-[You can play with this section]-=-=-=-=-=-=-=-
def random_y():
    return random.randint(0, 1200)
def random_x():
    return random.randint(0, 500)
def random_time():
    return random.randint(40, 600)
def random_size():
    return random.randint(300, 1500)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def set_window_to_top(window_name):
    hwnd = win32gui.FindWindow(None, window_name)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                           win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST | win32con.WS_EX_NOACTIVATE)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_NOACTIVATE | win32con.SWP_SHOWWINDOW)
def play_wav(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def main():
    video_path = 'resources/gnome.mp4'
    audio_path = 'resources/gnome.wav'
    win_size = random_size()
    # Initialize Pygame for audio
    pygame.init()

    # Start playing the audio
    play_wav(audio_path)

    # Capture video using OpenCV
    cap = cv2.VideoCapture(video_path)

    # Get frame dimensions
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    new_width = win_size+300
    new_height = win_size

    # Create window
    window_name = 'Dancing Gnome'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    set_window_to_top(window_name)
    random_xint = random_x()
    random_yint = random_y()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to 1/4 of the screen size
        frame = cv2.resize(frame, (new_width, new_height))

        # Convert the frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define the blue color range
        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        # Create a mask to filter out the blue color
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # Bitwise-AND mask and original image
        gnome = cv2.bitwise_and(frame, frame, mask=mask_inv)

        # Create a black background frame
        background = np.zeros_like(frame)

        # Bitwise-AND mask_inv and the black background
        background = cv2.bitwise_and(background, background, mask=mask)

        # Add the gnome to the background
        result = cv2.add(gnome, background)

        # Display the resulting frame
        cv2.imshow(window_name, result)

        # Position the window at the top-left corner
        hwnd = win32gui.FindWindow(None, window_name)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, random_yint, random_xint, new_width, new_height, win32con.SWP_NOACTIVATE | win32con.SWP_SHOWWINDOW)

        # Exit on ESC key
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Release everything
    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

def core():
    randnom_time = random_time()
    time.sleep(randnom_time)
    now = datetime.datetime.now()
    print('[',now,'] HAHAHA GNOME CRAWLING!!!!!!')
    main()
    core()

if __name__ == '__main__':
    print('Welcome to Wizard Gnome Desktop Pet. Enjoy!')
    core()
