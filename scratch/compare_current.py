import cv2
import numpy as np

before = cv2.imread('public/images/trans-hair-before.jpg')
after = cv2.imread('public/images/trans-hair-after.jpg')

# Crop face [180:680, 350:680]
crop_b = before[180:680, 350:680]
crop_a = after[180:680, 350:680]

comp = np.hstack([crop_b, crop_a])
# Add labels
cv2.putText(comp, "CURRENT BEFORE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
cv2.putText(comp, "AFTER (PRISTINE)", (350, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

cv2.imwrite('scratch/current_comparison.jpg', comp)
print("Saved scratch/current_comparison.jpg")
