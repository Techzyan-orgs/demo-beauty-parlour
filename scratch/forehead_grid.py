import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')

# Let's save a close-up of the forehead and eyes with 10px grid:
forehead_crop = img[180:360, 350:550].copy()
for x in range(0, 200, 10):
    cv2.line(forehead_crop, (x, 0), (x, 180), (128, 128, 128), 1)
    if x % 20 == 0:
        cv2.putText(forehead_crop, str(350 + x), (x, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)

for y in range(0, 180, 10):
    cv2.line(forehead_crop, (0, y), (200, y), (128, 128, 128), 1)
    if y % 20 == 0:
        cv2.putText(forehead_crop, str(180 + y), (5, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)

cv2.imwrite('scratch/forehead_tight_grid.jpg', forehead_crop)
print("Saved scratch/forehead_tight_grid.jpg")
