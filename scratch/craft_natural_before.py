import cv2
import numpy as np

# Load the pristine After image
img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img_after.shape
print(f"Loaded image: {w}x{h}")

# 1. Build a precise Facial Skin Mask
# We will construct an accurate polygon/ellipse mask for the face skin only,
# and exclude eyes, eyebrows, bindi, lips, earring, hair, mogra flowers, saree, background.

face_mask = np.zeros((h, w), dtype=np.float32)

# Main face contour (forehead down to jawline and neck)
# Forehead: y from 210 to 330, x from 370 to 520
# Cheeks: y from 330 to 550, x from 360 to 650
# Chin / Neck: y from 550 to 760, x from 430 to 670

# Let's define the outer face boundary polygon
pts_face = np.array([
    [375, 260],
    [395, 225],
    [430, 215],
    [470, 215],
    [515, 230],
    [550, 265],
    [590, 315],
    [635, 380],
    [645, 435],
    [640, 480],
    [655, 540], # neck start
    [670, 620],
    [670, 710],
    [630, 765],
    [540, 780],
    [455, 760],
    [440, 680],
    [420, 620],
    [390, 560],
    [360, 500],
    [355, 440],
    [360, 370],
    [365, 310]
], np.int32)

cv2.fillPoly(face_mask, [pts_face], 1.0)

# Soften the outer boundary
face_mask = cv2.GaussianBlur(face_mask, (21, 21), 0)

# Exclude Features from mask:
# A. Bindi at (412, 328)
bindi_mask = np.zeros((h, w), dtype=np.float32)
cv2.circle(bindi_mask, (412, 328), 9, 1.0, -1)
bindi_mask = cv2.GaussianBlur(bindi_mask, (5, 5), 0)
face_mask = face_mask * (1.0 - bindi_mask)

# B. Right eye (viewer left): x: 360..425, y: 350..400
eye_r_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(eye_r_mask, (395, 375), (28, 18), -5, 0, 360, 1.0, -1)
eye_r_mask = cv2.GaussianBlur(eye_r_mask, (11, 11), 0)
face_mask = face_mask * (1.0 - eye_r_mask)

# C. Left eye (viewer right): x: 450..560, y: 345..400
eye_l_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(eye_l_mask, (505, 372), (38, 20), 0, 0, 360, 1.0, -1)
eye_l_mask = cv2.GaussianBlur(eye_l_mask, (11, 11), 0)
face_mask = face_mask * (1.0 - eye_l_mask)

# D. Eyebrows
brow_mask = np.zeros((h, w), dtype=np.float32)
# viewer left eyebrow
cv2.ellipse(brow_mask, (390, 335), (25, 10), -20, 0, 360, 1.0, -1)
# viewer right eyebrow
cv2.ellipse(brow_mask, (510, 330), (50, 15), 5, 0, 360, 1.0, -1)
brow_mask = cv2.GaussianBlur(brow_mask, (11, 11), 0)
face_mask = face_mask * (1.0 - brow_mask)

# E. Lips / Mouth: x: 405..525, y: 535..610
lips_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(lips_mask, (465, 570), (45, 24), 0, 0, 360, 1.0, -1)
lips_mask = cv2.GaussianBlur(lips_mask, (11, 11), 0)
face_mask = face_mask * (1.0 - lips_mask)

# F. Earring: x: 640..690, y: 510..575
earring_mask = np.zeros((h, w), dtype=np.float32)
cv2.circle(earring_mask, (662, 542), 22, 1.0, -1)
earring_mask = cv2.GaussianBlur(earring_mask, (9, 9), 0)
face_mask = face_mask * (1.0 - earring_mask)

# G. Exclude anything outside actual skin color distribution (e.g. hair strands, background, saree)
# Hair is very dark in BGR: max(B,G,R) < 65
hair_detect = (np.max(img_after, axis=2) < 55).astype(np.float32)
hair_detect = cv2.dilate(hair_detect, np.ones((5, 5), np.uint8))
hair_detect = cv2.GaussianBlur(hair_detect, (9, 9), 0)
face_mask = face_mask * (1.0 - hair_detect)

# Save mask preview
cv2.imwrite('scratch/test_face_mask.jpg', (face_mask * 255).astype(np.uint8))

print("Mask generated successfully.")
