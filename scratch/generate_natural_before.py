import cv2
import numpy as np

# Load pristine After image
img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, c = img_after.shape
print(f"Loaded image: {w}x{h}")

# Convert to float and LAB color space
img_float = img_after.astype(np.float32)
lab = cv2.cvtColor(img_after, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[:, :, 0]
A = lab[:, :, 1]
B = lab[:, :, 2]

# ----------------------------------------------------
# 1. Base Face Skin Mask
# ----------------------------------------------------
raw_face = np.zeros((h, w), dtype=np.float32)

# Polygon covering face and neck
pts_face = np.array([
    [415, 250],
    [450, 230],
    [500, 225],
    [540, 240],
    [580, 280],
    [620, 335],
    [645, 385],
    [655, 440],
    [645, 485],
    [665, 540], # neck
    [680, 620],
    [670, 710],
    [630, 765],
    [540, 780],
    [455, 760],
    [440, 680],
    [420, 620],
    [390, 560],
    [360, 500],
    [355, 440],
    [365, 370],
    [380, 310]
], np.int32)
cv2.fillPoly(raw_face, [pts_face], 1.0)

# Protected feature solid mask: these areas MUST NOT be touched AT ALL (diff = 0)
protected_solid = np.zeros((h, w), dtype=np.float32)

# A. Bindi: (491, 325)
cv2.circle(protected_solid, (491, 325), 9, 1.0, -1)

# B. Viewer Left Eye (her right): (460, 355)
cv2.ellipse(protected_solid, (460, 355), (28, 20), -5, 0, 360, 1.0, -1)

# C. Viewer Right Eye (her left): (550, 350)
cv2.ellipse(protected_solid, (550, 350), (35, 20), 5, 0, 360, 1.0, -1)

# D. Eyebrows
cv2.ellipse(protected_solid, (440, 330), (22, 10), -20, 0, 360, 1.0, -1)
cv2.ellipse(protected_solid, (540, 320), (45, 14), 5, 0, 360, 1.0, -1)

# E. Lips: (499, 471)
cv2.ellipse(protected_solid, (499, 471), (46, 24), 2, 0, 360, 1.0, -1)

# F. Earring: (697, 423)
cv2.circle(protected_solid, (697, 423), 26, 1.0, -1)

# G. Hair & background & flowers (outside face)
# Hair detection: very dark pixels
hair_detect = (np.max(img_after, axis=2) < 65).astype(np.float32)
cv2.dilate(hair_detect, np.ones((5, 5), np.uint8), dst=hair_detect)
protected_solid = np.maximum(protected_solid, hair_detect)

# Left background: x < 350
protected_solid[:, :350] = 1.0

# Right flowers: x > 650, y > 380
protected_solid[380:, 650:] = 1.0

# Saree bottom: y > 780
protected_solid[780:, :] = 1.0

# Create smooth feathering away from protected regions
# Distance transform to ensure a smooth transition into skin
dist_from_protected = cv2.distanceTransform((1.0 - protected_solid).astype(np.uint8), cv2.DIST_L2, 5)
feather_in = np.clip(dist_from_protected / 15.0, 0.0, 1.0) # smooth 15-pixel ramp

# Distance transform from raw face boundary
dist_inside_face = cv2.distanceTransform(raw_face.astype(np.uint8), cv2.DIST_L2, 5)
feather_face = np.clip(dist_inside_face / 20.0, 0.0, 1.0)

# Final clean skin mask
face_mask = feather_face * feather_in
# Force strictly 0 in protected regions
face_mask[protected_solid > 0.0] = 0.0

print("Face mask generated. Min:", face_mask.min(), "Max:", face_mask.max())

# ----------------------------------------------------
# 2. De-glaze Dewy Glass-Skin Specular Highlight
# ----------------------------------------------------
# High cheekbone highlight zone: (595, 415), size (50, 35), angle 25 deg
cheek_hl = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(cheek_hl, (595, 415), (50, 35), 25, 0, 360, 1.0, -1)
cheek_hl = cv2.GaussianBlur(cheek_hl, (31, 31), 0)
cheek_hl = cheek_hl * face_mask

# ----------------------------------------------------
# 3. Soft Under-Eye Fatigue (Natural Mild Dark Circles)
# ----------------------------------------------------
undereye_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(undereye_mask, (460, 375), (18, 10), -5, 0, 360, 0.65, -1)
cv2.ellipse(undereye_mask, (550, 372), (25, 12), 5, 0, 360, 0.65, -1)
undereye_mask = cv2.GaussianBlur(undereye_mask, (15, 15), 0)
undereye_mask = undereye_mask * face_mask

# ----------------------------------------------------
# 4. Subtle, Natural Melanin Sun Spots / Blemishes (NOT black spots!)
# Warm caramel/melanin tones with soft Gaussian feathering
# ----------------------------------------------------
spots_layer_L = np.zeros((h, w), dtype=np.float32)
spots_layer_A = np.zeros((h, w), dtype=np.float32)
spots_layer_B = np.zeros((h, w), dtype=np.float32)

spot_coords = [
    # (x, y, radius, strength_L, strength_A, strength_B)
    (478, 435, 3.0, -14.0, 1.2, 2.0), # Right cheek sun speck
    (482, 442, 2.0, -12.0, 1.0, 1.8), # Sister micro-speck
    (565, 455, 3.5, -16.0, 1.5, 2.2), # Left mid-cheek melanin spot
    (558, 465, 2.5, -13.0, 1.0, 1.8), # Lower cheek speck
    (585, 375, 2.5, -14.0, 1.2, 2.0), # Temple/upper zygomatic mark
    (495, 525, 2.5, -15.0, 1.2, 2.0), # Chin natural beauty mark
    (438, 415, 2.0, -11.0, 1.0, 1.5), # Bridge of nose micro-speck
]

for sx, sy, srad, dL, dA, dB in spot_coords:
    spot_m = np.zeros((h, w), dtype=np.float32)
    cv2.circle(spot_m, (int(sx), int(sy)), int(round(srad)), 1.0, -1)
    spot_m = cv2.GaussianBlur(spot_m, (5, 5), 1.2)
    spots_layer_L += spot_m * dL
    spots_layer_A += spot_m * dA
    spots_layer_B += spot_m * dB

# ----------------------------------------------------
# 5. Apply Natural Tone Transformations to LAB
# ----------------------------------------------------
L_before = L.copy()
A_before = A.copy()
B_before = B.copy()

# A. Overall facial skin: reduce L by 8.5 points (bare untreated skin is slightly duller)
# and reduce warmth B by 2.2 points (untreated skin lacks the post-facial warm golden radiance)
L_before = L_before - face_mask * 8.5
B_before = B_before - face_mask * 2.2
A_before = A_before - face_mask * 0.5

# B. De-glaze specular cheek highlight (reduce high specular sheen to matte baseline)
high_specular = np.maximum(0.0, L_before - 155.0) / 100.0
L_before = L_before - (cheek_hl * 9.0 + cheek_hl * high_specular * 12.0)

# C. Apply under-eye fatigue
L_before = L_before + undereye_mask * (-10.5)
B_before = B_before + undereye_mask * 1.5 # slightly brownish orbital shadow

# D. Apply natural melanin spots
L_before = L_before + spots_layer_L * face_mask
A_before = A_before + spots_layer_A * face_mask
B_before = B_before + spots_layer_B * face_mask

# Clip to valid LAB ranges
L_before = np.clip(L_before, 0.0, 255.0)
A_before = np.clip(A_before, 0.0, 255.0)
B_before = np.clip(B_before, 0.0, 255.0)

# Reconstruct BGR image
lab_before = np.stack([L_before, A_before, B_before], axis=2).astype(np.uint8)
bgr_modified = cv2.cvtColor(lab_before, cv2.COLOR_LAB2BGR)

# Final strict blend: ONLY face_mask > 0 can differ from img_after
# Where face_mask == 0, GUARANTEED bit-exact to img_after
face_mask_3c = np.repeat(face_mask[:, :, np.newaxis], 3, axis=2)
img_before_final = np.clip(
    img_after.astype(np.float32) * (1.0 - face_mask_3c) + 
    bgr_modified.astype(np.float32) * face_mask_3c,
    0, 255
).astype(np.uint8)

# Wherever protected_solid is > 0, enforce 100% bit-exact copy
img_before_final[protected_solid > 0] = img_after[protected_solid > 0]

# ----------------------------------------------------
# 6. Verification Metrics
# ----------------------------------------------------
diff = np.abs(img_after.astype(np.int16) - img_before_final.astype(np.int16))
non_zero_diff = np.sum(diff > 0)
total_pixels = h * w * c
print(f"Total pixels modified: {non_zero_diff} / {total_pixels} ({non_zero_diff / total_pixels * 100:.2f}%)")

# Check that non-face regions are 100% exact (diff == 0)
assert np.max(diff[:200, :300]) == 0, "Background altered!"
assert np.max(diff[820:, :]) == 0, "Saree bottom altered!"
assert np.max(diff[450:600, 700:]) == 0, "Mogra flowers altered!"
assert np.max(diff[410:435, 685:710]) == 0, "Earring altered!"
assert np.max(diff[322:328, 488:494]) == 0, "Bindi altered!"
assert np.max(diff[465:475, 490:510]) == 0, "Lips altered!"
assert np.max(diff[342:352, 458:468]) == 0, "Left eye pupil altered!"
assert np.max(diff[341:351, 539:549]) == 0, "Right eye pupil altered!"

print("All assertion checks PASSED! Non-skin regions are 100% bit-identical.")

# Save test result & side-by-side comparison crop
cv2.imwrite('scratch/natural_before_full.jpg', img_before_final, [cv2.IMWRITE_JPEG_QUALITY, 96])

# Make side-by-side face crop for visual inspection:
crop_y1, crop_y2, crop_x1, crop_x2 = 220, 640, 360, 680
face_after = img_after[crop_y1:crop_y2, crop_x1:crop_x2]
face_before = img_before_final[crop_y1:crop_y2, crop_x1:crop_x2]

labeled_before = face_before.copy()
cv2.putText(labeled_before, "BEFORE (Bare Skin)", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
labeled_after = face_after.copy()
cv2.putText(labeled_after, "AFTER (Bridal Glow)", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

comp_side_by_side = np.hstack([labeled_before, labeled_after])
cv2.imwrite('scratch/comp_before_after_face.jpg', comp_side_by_side, [cv2.IMWRITE_JPEG_QUALITY, 95])
print("Saved scratch/comp_before_after_face.jpg")
