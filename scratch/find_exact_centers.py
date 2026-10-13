import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')

# Let's save crops centered around key points to visually confirm each one:
# 1. Bindi: let's test around (450..470, 300..330)
cv2.imwrite('scratch/test_bindi_window.jpg', img[290:340, 440:480])

# 2. Left eye (viewer left):
cv2.imwrite('scratch/test_lefteye_window.jpg', img[330:400, 410:480])

# 3. Right eye (viewer right):
cv2.imwrite('scratch/test_righteye_window.jpg', img[330:400, 500:580])

# 4. Lips:
cv2.imwrite('scratch/test_lips_window.jpg', img[480:560, 440:560])

# 5. Cheek highlight:
cv2.imwrite('scratch/test_cheek_window.jpg', img[380:480, 540:660])

# 6. Earring:
cv2.imwrite('scratch/test_earring_window.jpg', img[420:500, 680:740])

print("Saved all 6 windows!")
