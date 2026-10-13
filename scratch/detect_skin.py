import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img.shape
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
L = lab[:, :, 0]
A = lab[:, :, 1]
B = lab[:, :, 2]

# True skin condition:
# Skin in this lighting: L in [100, 240], A in [132, 158], B in [134, 168]
# And R > G > B
b, g, r = cv2.split(img)
is_skin_color = (
    (L >= 100) & (L <= 245) &
    (A >= 132) & (A <= 158) &
    (B >= 134) & (B <= 168) &
    (r.astype(int) - b.astype(int) >= 30) &
    (g.astype(int) - b.astype(int) >= 10)
)

# Spatial bounding box of face & neck:
spatial_box = np.zeros((h, w), dtype=bool)
spatial_box[220:650, 360:645] = True

# Combined true skin mask
true_skin = is_skin_color & spatial_box

# Remove eyes, bindi, lips, earring from true skin:
# Let's verify eye locations:
# Left eye (viewer left): x: 395..440, y: 345..370
# Right eye (viewer right): x: 505..555, y: 340..370
# Bindi: x: 463..472, y: 308..316
# Lips: x: 420..510, y: 485..540
# Earring: x: 635..675, y: 450..510

features_mask = np.zeros((h, w), dtype=bool)
# Eyes
features_mask[345:370, 395:440] = True
features_mask[340:370, 505:555] = True
# Bindi
features_mask[308:316, 463:472] = True
# Lips
features_mask[485:540, 420:510] = True
# Earring
features_mask[450:510, 635:675] = True

bare_skin = true_skin & (~features_mask)

# Save visualization of bare skin
vis = img.copy()
vis[bare_skin] = [0, 255, 0]
cv2.imwrite('scratch/detected_bare_skin.jpg', vis[180:680, 350:680])
print(f"Total bare skin pixels: {np.sum(bare_skin)}")
