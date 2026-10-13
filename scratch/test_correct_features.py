import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
test = img.copy()

# Exact coordinates
# 1. Bindi: (412, 320)
cv2.circle(test, (412, 320), 8, (0, 0, 255), 2)

# 2. Left eye (viewer left): x: 375..425, y: 355..395
cv2.rectangle(test, (375, 355), (425, 395), (0, 255, 0), 2)

# 3. Right eye (viewer right): x: 495..570, y: 345..395
cv2.rectangle(test, (495, 345), (570, 395), (0, 255, 0), 2)

# 4. Lips: x: 395..505, y: 500..565
cv2.rectangle(test, (395, 500), (505, 565), (255, 255, 0), 2)

# 5. Earring: x: 640..675, y: 460..515
cv2.rectangle(test, (640, 460), (675, 515), (255, 0, 255), 2)

# 6. Main cheek highlight zone: x: 480..610, y: 395..495
cv2.rectangle(test, (480, 395), (610, 495), (0, 255, 255), 2)

cv2.imwrite('scratch/correct_features_test.jpg', test[200:680, 340:700])
print("Saved scratch/correct_features_test.jpg")
