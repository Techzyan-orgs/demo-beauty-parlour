import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img.shape
print(f"Image shape: {w}x{h}")

# Let's draw a grid over the face region [150:750, 350:750] with 50-pixel spacing and coordinate labels
vis = img.copy()
for x in range(350, 750, 25):
    cv2.line(vis, (x, 150), (x, 750), (100, 100, 100), 1)
    if x % 50 == 0:
        cv2.putText(vis, str(x), (x, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

for y in range(150, 750, 25):
    cv2.line(vis, (350, y), (750, y), (100, 100, 100), 1)
    if y % 50 == 0:
        cv2.putText(vis, str(y), (360, y), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

cv2.imwrite('scratch/grid_coords.jpg', vis[150:750, 350:750])
print("Saved scratch/grid_coords.jpg")
