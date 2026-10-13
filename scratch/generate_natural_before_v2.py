import cv2
import numpy as np

# Load pristine After image
img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, c = img_after.shape
print(f"Loaded image: {w}x{h}")

# Convert to float and LAB
lab = cv2.cvtColor(img_after, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[:, :, 0]
A = lab[:, :, 1]
B = lab[:, :, 2]

# ----------------------------------------------------
# 1. Base Face Skin Mask
# ----------------------------------------------------
raw_face = np.zeros((h, w), dtype=np.float32)

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

# Protected feature solid mask: strictly 0 diff
protected_solid = np.zeros((h, w), dtype=np.float32)

# A. Bindi: (491, 325)
cv2.circle(protected_solid, (491, 325), 9, 1.0, -1)

# B. Left Eye (viewer left): (460, 355)
cv2.ellipse(protected_solid, (460, 355), (28, 20), -5, 0, 360, 1.0, -1)

# C. Right Eye (viewer right): (550, 350)
cv2.ellipse(protected_solid, (550, 350), (35, 20), 5, 0, 360, 1.0, -1)

# D. Eyebrows
cv2.ellipse(protected_solid, (440, 330), (22, 10), -20, 0, 360, 1.0, -1)
cv2.ellipse(protected_solid, (540, 320), (45, 14), 5, 0, 360, 1.0, -1)

# E. Lips: (499, 471)
cv2.ellipse(protected_solid, (499, 471), (46, 24), 2, 0, 360, 1.0, -1)

# F. Earring: (697, 423)
cv2.circle(protected_solid, (697, 423), 26, 1.0, -1)

# G. Hair & background & flowers
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
dist_from_protected = cv2.distanceTransform((1.0 - protected_solid).astype(np.uint8), cv2.DIST_L2, 5)
feather_in = np.clip(dist_from_protected / 15.0, 0.0, 1.0)

dist_inside_face = cv2.distanceTransform(raw_face.astype(np.uint8), cv2.DIST_L2, 5)
feather_face = np.clip(dist_inside_face / 20.0, 0.0, 1.0)

face_mask = feather_face * feather_in
face_mask[protected_solid > 0.0] = 0.0

# ----------------------------------------------------
# 2. De-glaze Dewy Glass-Skin Specular Highlight
# ----------------------------------------------------
# In the After image, cheekbone (595, 415) has a glowing glass highlight.
# For untreated bare skin, de-glaze it to a matte, non-shiny finish.
cheek_hl = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(cheek_hl, (595, 415), (55, 38), 25, 0, 360, 1.0, -1)
cheek_hl = cv2.GaussianBlur(cheek_hl, (31, 31), 0)
cheek_hl = cheek_hl * face_mask

# Forehead center highlight:
forehead_hl = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(forehead_hl, (490, 260), (35, 20), 0, 0, 360, 1.0, -1)
forehead_hl = cv2.GaussianBlur(forehead_hl, (25, 25), 0)
forehead_hl = forehead_hl * face_mask

# ----------------------------------------------------
# 3. Soft Under-Eye Fatigue (Natural Pre-Bridal Dark Circles)
# ----------------------------------------------------
undereye_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(undereye_mask, (460, 375), (20, 11), -5, 0, 360, 0.8, -1)
cv2.ellipse(undereye_mask, (550, 372), (28, 14), 5, 0, 360, 0.8, -1)
undereye_mask = cv2.GaussianBlur(undereye_mask, (15, 15), 0)
undereye_mask = undereye_mask * face_mask

# ----------------------------------------------------
# 4. Realistic Sun Spots & Natural Blemishes (WARM MELANIN, NOT BLACK)
# ----------------------------------------------------
# Sun spots and mild pigmentation marks in authentic warm-brown melanin tones
spots_layer_L = np.zeros((h, w), dtype=np.float32)
spots_layer_A = np.zeros((h, w), dtype=np.float32)
spots_layer_B = np.zeros((h, w), dtype=np.float32)

# Coordinates for natural skin blemishes & sun freckles:
# (x, y, radius, dL, dA, dB)
# dL: -20 to -26 (clearly visible natural sun spots / freckles, NOT black ink)
# dA: +1.8 to +2.5 (warm reddish-brown melanin undertone)
# dB: +3.0 to +4.5 (golden-brown / caramel melanin tone)
spot_specs = [
    # Right cheek cluster (viewer left)
    (476, 432, 4.0, -24.0, 2.0, 3.5), # Main right cheek sun spot
    (482, 440, 3.0, -20.0, 1.8, 3.0), # Minor satellite freckle
    (470, 448, 2.5, -18.0, 1.5, 2.5), # Lower speck
    # Left cheek / high cheekbone (viewer right)
    (562, 445, 4.5, -25.0, 2.2, 4.0), # Left cheek sun spot / blemish
    (572, 458, 3.2, -22.0, 1.8, 3.2), # Secondary cheek pigment mark
    (554, 468, 2.8, -19.0, 1.5, 2.8), # Mild pigment mark
    # Temple / upper cheek
    (588, 380, 3.5, -22.0, 2.0, 3.5), # Temple sun freckle
    # Bridge of nose
    (470, 405, 2.5, -18.0, 1.5, 2.5), # Bridge sun freckle
    # Jawline natural beauty mark
    (515, 525, 3.2, -24.0, 2.0, 3.5), # Natural jawline mole / beauty mark
]

for sx, sy, srad, dL, dA, dB in spot_specs:
    spot_m = np.zeros((h, w), dtype=np.float32)
    # Organic slightly irregular shape: two overlapping tiny circles
    cv2.circle(spot_m, (int(sx), int(sy)), int(round(srad)), 1.0, -1)
    cv2.circle(spot_m, (int(sx + 1), int(sy)), int(round(max(1.0, srad - 1.0))), 0.8, -1)
    spot_m = cv2.GaussianBlur(spot_m, (5, 5), 1.2)
    spots_layer_L += spot_m * dL
    spots_layer_A += spot_m * dA
    spots_layer_B += spot_m * dB

# ----------------------------------------------------
# 5. Mild Tone Unevenness / Melasma (Organic diffuse cloud)
# ----------------------------------------------------
# Realistic bare skin has subtle tone unevenness on the cheeks from sun exposure
uneven_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(uneven_mask, (565, 435), (40, 25), 15, 0, 360, 0.4, -1)
cv2.ellipse(uneven_mask, (475, 430), (25, 18), -10, 0, 360, 0.35, -1)
uneven_mask = cv2.GaussianBlur(uneven_mask, (35, 35), 0)
uneven_mask = uneven_mask * face_mask

# ----------------------------------------------------
# 6. Apply Natural Transformations to LAB
# ----------------------------------------------------
L_before = L.copy()
A_before = A.copy()
B_before = B.copy()

# A. Overall facial skin dullness:
# Untreated skin has lower luminosity (-11.5) and slightly less fresh golden radiance (B -1.5)
L_before = L_before - face_mask * 11.5
B_before = B_before - face_mask * 1.5

# B. De-glaze high specular dewy highlights (removes the "glass skin" serum shine)
specular_reduction = cheek_hl * 12.0 + forehead_hl * 8.0
# Extra suppression of high-luminance peaks (L > 155)
high_spec = np.maximum(0.0, L_before - 150.0) / 80.0
specular_reduction += cheek_hl * high_spec * 14.0
L_before = L_before - specular_reduction

# C. Natural Under-Eye Fatigue (soft dark circles)
L_before = L_before + undereye_mask * (-14.0)
B_before = B_before + undereye_mask * 2.0 # subtle warm brownish under-eye shadow

# D. Mild tone unevenness across cheekbones
L_before = L_before + uneven_mask * (-6.0)
B_before = B_before + uneven_mask * 1.5

# E. Natural spots & blemishes
L_before = L_before + spots_layer_L * face_mask
A_before = A_before + spots_layer_A * face_mask
B_before = B_before + spots_layer_B * face_mask

# Clip to valid LAB range
L_before = np.clip(L_before, 0.0, 255.0)
A_before = np.clip(A_before, 0.0, 255.0)
B_before = np.clip(B_before, 0.0, 255.0)

# Reconstruct BGR
lab_before = np.stack([L_before, A_before, B_before], axis=2).astype(np.uint8)
bgr_modified = cv2.cvtColor(lab_before, cv2.COLOR_LAB2BGR)

# Blend with face mask
face_mask_3c = np.repeat(face_mask[:, :, np.newaxis], 3, axis=2)
img_before_final = np.clip(
    img_after.astype(np.float32) * (1.0 - face_mask_3c) + 
    bgr_modified.astype(np.float32) * face_mask_3c,
    0, 255
).astype(np.uint8)

# Strictly enforce bit-exact preservation on all protected areas
img_before_final[protected_solid > 0] = img_after[protected_solid > 0]

# ----------------------------------------------------
# 7. Verification & Export
# ----------------------------------------------------
diff = np.abs(img_after.astype(np.int16) - img_before_final.astype(np.int16))
non_zero_diff = np.sum(diff > 0)
total_pixels = h * w * c
print(f"Total pixels modified: {non_zero_diff} / {total_pixels} ({non_zero_diff / total_pixels * 100:.2f}%)")

# Verify non-skin regions are 100% exact
assert np.max(diff[:200, :300]) == 0, "Background altered!"
assert np.max(diff[820:, :]) == 0, "Saree bottom altered!"
assert np.max(diff[450:600, 700:]) == 0, "Mogra flowers altered!"
assert np.max(diff[410:435, 685:710]) == 0, "Earring altered!"
assert np.max(diff[322:328, 488:494]) == 0, "Bindi altered!"
assert np.max(diff[465:475, 490:510]) == 0, "Lips altered!"
assert np.max(diff[342:352, 458:468]) == 0, "Left eye pupil altered!"
assert np.max(diff[341:351, 539:549]) == 0, "Right eye pupil altered!"

print("All assertions PASSED! Protected areas are bit-exact.")

# Save full Before image candidate
cv2.imwrite('scratch/natural_before_v2.jpg', img_before_final, [cv2.IMWRITE_JPEG_QUALITY, 96])

# Make side-by-side comparison crop
crop_y1, crop_y2, crop_x1, crop_x2 = 220, 640, 360, 680
face_after = img_after[crop_y1:crop_y2, crop_x1:crop_x2]
face_before = img_before_final[crop_y1:crop_y2, crop_x1:crop_x2]

labeled_before = face_before.copy()
cv2.putText(labeled_before, "BEFORE (Bare Skin)", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
labeled_after = face_after.copy()
cv2.putText(labeled_after, "AFTER (Bridal Glow)", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

comp_side_by_side = np.hstack([labeled_before, labeled_after])
cv2.imwrite('scratch/comp_before_after_v2.jpg', comp_side_by_side, [cv2.IMWRITE_JPEG_QUALITY, 95])
print("Saved scratch/comp_before_after_v2.jpg")
