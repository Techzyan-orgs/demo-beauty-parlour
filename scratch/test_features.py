import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
test = img.copy()

# Add (+44 in x, +32 in y)
# 1. Bindi
cv2.circle(test, (494, 333), 6, (0, 0, 255), 2)

# 2. Left eye (her right eye, viewer left)
cv2.rectangle(test, (470, 360), (525, 415), (0, 255, 0), 2)

# 3. Right eye (her left eye, viewer right)
cv2.rectangle(test, (550, 350), (625, 415), (0, 255, 0), 2)

# 4. Lips
cv2.rectangle(test, (475, 510), (595, 580), (255, 255, 0), 2)

# 5. Earring
cv2.circle(test, (695, 485), 18, (255, 0, 255), 2)

cv2.imwrite('scratch/shifted_features_test.jpg', test[200:750, 400:750])
print("Saved scratch/shifted_features_test.jpg")
