import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import ctypes
import math
import keyboard  # for emergency exit

# ========== CONFIG ==========
dead_zone = 50  # Neutral zone radius
move_speed = 25  # Speed of mouse movement
click_threshold = 40  # Distance in pixels to trigger click
# ============================

# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Enable multi-monitor awareness
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
screen_w = user32.GetSystemMetrics(78)
screen_h = user32.GetSystemMetrics(79)
screen_x = user32.GetSystemMetrics(76)
screen_y = user32.GetSystemMetrics(77)

# Setup camera
cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
detector = HandDetector(detectionCon=0.7, maxHands=1)

clicking = False

while True:
    success, img = cap.read()
    if not success:
        continue

    img = cv2.flip(img, 1)
    hands, _ = detector.findHands(img)

    frame_h, frame_w, _ = img.shape
    center_x = frame_w // 2
    center_y = frame_h // 2

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        index_x, index_y = lmList[8][0], lmList[8][1]

        # ========== MOUSE MOVEMENT ==========
        dx = index_x - center_x
        dy = index_y - center_y

        if abs(dx) > dead_zone or abs(dy) > dead_zone:
            curr_x, curr_y = pyautogui.position()

            if dx < -dead_zone:
                curr_x -= move_speed
            elif dx > dead_zone:
                curr_x += move_speed

            if dy < -dead_zone:
                curr_y -= move_speed
            elif dy > dead_zone:
                curr_y += move_speed

            # Clamp across all monitors
            curr_x = max(screen_x, min(screen_x + screen_w - 1, curr_x))
            curr_y = max(screen_y, min(screen_y + screen_h - 1, curr_y))
            pyautogui.moveTo(curr_x, curr_y)

        # ========== CLICKING ==========
        thumb_x, thumb_y = lmList[4][0], lmList[4][1]
        mid_x, mid_y = lmList[12][0], lmList[12][1]

        distance = math.hypot(mid_x - thumb_x, mid_y - thumb_y)

        if distance < click_threshold and not clicking:
            clicking = True
            pyautogui.click()
            print("🖱️ Click!")

        elif distance >= click_threshold:
            clicking = False

        # Optional UI overlay
        cv2.circle(img, (center_x, center_y), dead_zone, (255, 0, 0), 2)
        cv2.circle(img, (index_x, index_y), 10, (0, 255, 0), -1)

    # Show frame (optional)
    cv2.imshow("Joystick Gesture Control", img)

    # Exit on 'q' or Esc key
    if cv2.waitKey(1) == ord("q") or keyboard.is_pressed("esc"):
        print("🛑 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
