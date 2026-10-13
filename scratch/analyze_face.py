import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img.shape
print(f"Loaded image: shape={img.shape}")

# Look at scratch/all_features_verified.jpg:
# In scratch/all_features_verified.jpg we cropped img[200:660, 350:690]
# The bride's face is inside this crop!
# In the crop:
# Her left eye (viewer's right) had box (495, 310) to (580, 385).
# That box fit HER left eye perfectly!
# Now her other eye (viewer's left):
# In all_features_verified.jpg, the green box (380, 310) to (455, 385) was too far left.
# Her actual right eye (viewer's left) is around x: 420 to 480, y: 320 to 380!
# And the bindi is between the eyebrows around x: 445 to 455, y: 315 to 325!
# Her lips:
# The cyan box (460, 450) to (580, 525) fit the lips well, but was slightly shifted right.
# Her mouth is around x: 430 to 540, y: 460 to 540!
# Her earring:
# The magenta box (635, 450) to (680, 520) was below the earlobe!
# The earring is actually at x: 640 to 675, y: 450 to 500!

# Let's verify by saving a precise overlay
test = img.copy()

# Bindi search
gray = cv2.cvtColor(img[300:335, 430:465], cv2.COLOR_BGR2GRAY)
_, max_v, _, max_loc = cv2.minMaxLoc(gray)
bindi_x = 430 + max_loc[0]
bindi_y = 300 + max_loc[1]
print(f"Exact bindi: ({bindi_x}, {bindi_y}) with max_val={max_v}")
cv2.circle(test, (bindi_x, bindi_y), 6, (0, 0, 255), 2)

# Eye left (viewer left)
cv2.rectangle(test, (425, 325), (475, 380), (0, 255, 0), 2)
# Eye right (viewer right)
cv2.rectangle(test, (505, 320), (575, 380), (0, 255, 0), 2)

# Lips
cv2.rectangle(test, (430, 470), (540, 540), (255, 255, 0), 2)

# Earring
cv2.rectangle(test, (640, 450), (675, 500), (255, 0, 255), 2)

cv2.imwrite('scratch/precise_features_test.jpg', test[200:660, 350:690])
print("Saved scratch/precise_features_test.jpg")
