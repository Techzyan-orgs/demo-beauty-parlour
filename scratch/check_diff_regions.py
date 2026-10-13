import cv2
import numpy as np

img_after = cv2.imread('public/images/trans-hair-after.jpg')
img_before = cv2.imread('public/images/trans-hair-before.jpg')

diff = np.abs(img_before.astype(int) - img_after.astype(int))
print(f"Max diff: {diff.max()}")
print(f"Mean diff where changed: {diff[diff > 0].mean() if np.any(diff > 0) else 0}")

# Check diff at specific regions:
# Forehead: y: 220..270, x: 420..500
forehead_diff = diff[220:270, 420:500]
print(f"Forehead diff max: {forehead_diff.max()}, mean: {forehead_diff.mean():.2f}")

# Under-eye: y: 370..385, x: 510..550
undereye_diff = diff[370:385, 510:550]
print(f"Under-eye diff max: {undereye_diff.max()}, mean: {undereye_diff.mean():.2f}")

# Cheek highlight: y: 400..440, x: 570..610
cheek_diff = diff[400:440, 570:610]
print(f"Cheek highlight diff max: {cheek_diff.max()}, mean: {cheek_diff.mean():.2f}")

# Let's save a visualization of the difference map amplified by 5x
diff_vis = np.clip(diff * 5, 0, 255).astype(np.uint8)
cv2.imwrite('scratch/diff_vis_5x.jpg', diff_vis[180:680, 350:680])
print("Saved scratch/diff_vis_5x.jpg")
