import cv2
import numpy as np

# Load pristine After image
img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img_after.shape
print(f"Loaded image: {w}x{h}")

lab = cv2.cvtColor(img_after, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[:, :, 0]
A = lab[:, :, 1]
B = lab[:, :, 2]

# --- 1. SEGMENTATION & SKIN MASK ---
# Skin color range in LAB for Indian bridal complexion:
# Generally L in 100..230, A in 130..160, B in 132..170
color_skin = (
    (L >= 80) & (L <= 245) &
    (A >= 132) & (A <= 162) &
    (B >= 133) & (B <= 172)
).astype(np.float32)

# Facial region mask (smooth polygon enclosing forehead, cheeks, nose, chin, neck)
face_poly = np.array([
    [375, 205], [440, 195], [510, 205], [545, 235],
    [580, 275], [615, 340], [635, 410], [640, 480],
    [620, 530], [580, 560], [560, 600], [580, 680],
    [540, 710], [440, 710], [430, 600], [390, 550],
    [360, 500], [345, 430], [355, 360], [360, 290]
], dtype=np.int32)

face_spatial = np.zeros((h, w), dtype=np.float32)
cv2.fillPoly(face_spatial, [face_poly], 1.0)
face_spatial = cv2.GaussianBlur(face_spatial, (31, 31), 0)

# Combine spatial + color gating
skin_mask = face_spatial * color_skin
skin_mask = cv2.GaussianBlur(skin_mask, (9, 9), 0)

# Exclude sensitive features (diff = 0 protection):
# Eyebrows & Eyes:
# Left eye + brow (viewer left): x: 360..450, y: 295..375
# Right eye + brow (viewer right): x: 470..595, y: 285..375
# Bindi: (457, 312)
# Lips: x: 400..520, y: 475..540
# Earring: x: 635..675, y: 450..510
protect_mask = np.zeros((h, w), dtype=np.float32)

# Viewer left eye
cv2.ellipse(protect_mask, (413, 356), (28, 18), -5, 0, 360, 1.0, -1)
# Viewer right eye
cv2.ellipse(protect_mask, (527, 352), (32, 19), 5, 0, 360, 1.0, -1)
# Viewer left brow
cv2.ellipse(protect_mask, (405, 312), (35, 12), -10, 0, 360, 1.0, -1)
# Viewer right brow
cv2.ellipse(protect_mask, (535, 305), (42, 14), 10, 0, 360, 1.0, -1)
# Bindi
cv2.circle(protect_mask, (457, 312), 10, 1.0, -1)
# Lips
cv2.ellipse(protect_mask, (455, 508), (48, 22), 2, 0, 360, 1.0, -1)
# Earring
cv2.circle(protect_mask, (655, 475), 26, 1.0, -1)

protect_mask = cv2.GaussianBlur(protect_mask, (11, 11), 0)
# Subtractive protection:
skin_mask = np.clip(skin_mask * (1.0 - protect_mask), 0.0, 1.0)

# Also hard zero outer non-skin regions for 100% diff=0 safety:
hard_zero = np.zeros((h, w), dtype=bool)
hard_zero[:190, :] = True
hard_zero[:, :340] = True
hard_zero[720:, :] = True
hard_zero[370:, 640:] = True  # Earring & flowers
skin_mask[hard_zero] = 0.0

print(f"Skin mask max: {skin_mask.max()}, mean in face: {skin_mask[300:500, 450:600].mean():.2f}")

# --- 2. DE-GLAZE SPECULAR HIGHLIGHTS & MATTE/DULL COMPLEXION ---
# Cheek specular highlight centered at (580, 415), axes (45, 35)
# Nose highlight along bridge (455, 360..430)
spec_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(spec_mask, (580, 415), (50, 40), 15, 0, 360, 1.0, -1)
cv2.ellipse(spec_mask, (455, 390), (16, 40), -5, 0, 360, 0.7, -1)
spec_mask = cv2.GaussianBlur(spec_mask, (25, 25), 0) * skin_mask

# Specular suppression: where L is bright (L > 140)
spec_excess = np.maximum(0.0, L - 140.0)
spec_suppression = spec_excess * 0.40 * spec_mask

# General skin dullness (untreated bare skin without radiant serum)
# Reduces L by ~10 on cheek & forehead, slightly lowers golden radiance (B -2.0)
general_dullness = 10.0 * skin_mask
L_work = L - (spec_suppression + general_dullness)
B_work = B - (2.0 * skin_mask)
A_work = A.copy()

# --- 3. KOLKATA SUN TAN & TONAL UNEVENNESS ---
# Forehead tanning and perimeter cheek tanning:
tan_mask = np.zeros((h, w), dtype=np.float32)
# Forehead tan
cv2.ellipse(tan_mask, (445, 245), (65, 30), 0, 0, 360, 1.0, -1)
# Outer cheek / temple tan (viewer right)
cv2.ellipse(tan_mask, (595, 370), (35, 65), 10, 0, 360, 0.9, -1)
# Outer cheek (viewer left)
cv2.ellipse(tan_mask, (380, 420), (25, 45), -10, 0, 360, 0.7, -1)
tan_mask = cv2.GaussianBlur(tan_mask, (35, 35), 0) * skin_mask

# Apply Tan: L reduced by 15.0, warmer melanin tone (dA +1.5, dB +2.8)
L_work = L_work - (15.0 * tan_mask)
A_work = A_work + (1.5 * tan_mask)
B_work = B_work + (2.8 * tan_mask)

# --- 4. UNDER-EYE FATIGUE / DARK CIRCLES ---
# Realistic pre-wedding fatigue in orbital hollows
undereye_mask = np.zeros((h, w), dtype=np.float32)
# Viewer left under-eye (415, 380)
cv2.ellipse(undereye_mask, (415, 380), (24, 11), -5, 0, 360, 1.0, -1)
# Viewer right under-eye (530, 377)
cv2.ellipse(undereye_mask, (530, 377), (26, 12), 5, 0, 360, 1.0, -1)
undereye_mask = cv2.GaussianBlur(undereye_mask, (15, 15), 0) * skin_mask

# Apply Dark Circles: L -18.0, dA +1.5, dB +0.5 (tired orbital venous shadow)
L_work = L_work - (18.0 * undereye_mask)
A_work = A_work + (1.5 * undereye_mask)
B_work = B_work + (0.5 * undereye_mask)

# --- 5. AUTHENTIC SUN SPOTS & ACNE BLEMISH MARKS ---
# Noticeable at normal zoom! 3 to 6 px diameter. Warm melanin / caramel brown.
# We create organic shaped spot masks with Gaussian feathering (sigma 1.0 - 1.4)
spots_L = np.zeros((h, w), dtype=np.float32)
spots_A = np.zeros((h, w), dtype=np.float32)
spots_B = np.zeros((h, w), dtype=np.float32)

# Spots list: (x, y, radius_x, radius_y, angle, dL, dA, dB)
# dL -26 to -32, dA +2 to +3, dB +3.5 to +5
blemishes = [
    # 1. High cheekbone sun spot (viewer right) - very noticeable
    (580, 420, 2.8, 2.3, 20, -30.0, 2.8, 4.5),
    # 2. Apple of cheek blemish mark (viewer right)
    (542, 442, 2.6, 2.2, -15, -28.0, 2.5, 4.2),
    # 3. Lower cheek post-inflammatory hyperpigmentation (viewer right)
    (568, 472, 2.4, 2.0, 40, -27.0, 2.4, 4.0),
    # 4. Temple sun freckle (viewer right)
    (598, 342, 2.5, 2.2, 0, -29.0, 2.6, 4.2),
    # 5. Forehead sun spot 1
    (472, 248, 2.8, 2.4, -20, -30.0, 2.7, 4.5),
    # 6. Forehead sun spot 2
    (422, 262, 2.3, 2.0, 10, -26.0, 2.3, 3.8),
    # 7. Viewer left cheek blemish mark
    (386, 432, 2.7, 2.3, 30, -29.0, 2.6, 4.3),
    # 8. Viewer left lower cheek
    (376, 460, 2.4, 2.0, -10, -26.0, 2.2, 3.8),
    # 9. Flank of nose sun freckle
    (482, 412, 2.3, 2.0, 15, -27.0, 2.4, 4.0),
    # 10. Jawline authentic beauty mark / blemish
    (522, 538, 2.8, 2.4, -30, -30.0, 2.8, 4.5),
]

for sx, sy, rx, ry, ang, dL, dA, dB in blemishes:
    s_mask = np.zeros((h, w), dtype=np.float32)
    cv2.ellipse(s_mask, (int(sx), int(sy)), (int(round(rx)), int(round(ry))), ang, 0, 360, 1.0, -1)
    # Add a tiny irregular secondary satellite to make it organic, not a machine stamp
    cv2.circle(s_mask, (int(sx + np.sign(ang)*1), int(sy + 1)), max(1, int(round(rx * 0.6))), 0.8, -1)
    s_mask = cv2.GaussianBlur(s_mask, (7, 7), 1.1)
    # Normalize peak to 1.0
    if s_mask.max() > 0:
        s_mask = s_mask / s_mask.max()
    spots_L += s_mask * dL
    spots_A += s_mask * dA
    spots_B += s_mask * dB

L_work = L_work + (spots_L * skin_mask)
A_work = A_work + (spots_A * skin_mask)
B_work = B_work + (spots_B * skin_mask)

# Clip LAB channels
L_final = np.clip(L_work, 0.0, 255.0)
A_final = np.clip(A_work, 0.0, 255.0)
B_final = np.clip(B_work, 0.0, 255.0)

lab_out = np.stack([L_final, A_final, B_final], axis=2).astype(np.uint8)
bgr_out = cv2.cvtColor(lab_out, cv2.COLOR_LAB2BGR)

# Composite strictly with skin_mask
skin_mask_3c = np.repeat(skin_mask[:, :, np.newaxis], 3, axis=2)
img_before_result = np.clip(
    img_after.astype(np.float32) * (1.0 - skin_mask_3c) +
    bgr_out.astype(np.float32) * skin_mask_3c,
    0, 255
).astype(np.uint8)

# Strict non-skin preservation: bit-exact diff = 0
diff_map = np.abs(img_before_result.astype(int) - img_after.astype(int))
changed_pixels = np.any(diff_map > 0, axis=2)

# Ensure non-skin regions are strictly bit-exact:
img_before_result[hard_zero] = img_after[hard_zero]
img_before_result[protect_mask > 0.05] = img_after[protect_mask > 0.05]

# Final diff check
final_diff = np.abs(img_before_result.astype(int) - img_after.astype(int))
print(f"Total changed pixels: {np.sum(np.any(final_diff > 0, axis=2))}")
print(f"Max diff in background/hair/jewels: {final_diff[hard_zero].max()}")

# Save trial before
cv2.imwrite('scratch/trial_before.jpg', img_before_result, [cv2.IMWRITE_JPEG_QUALITY, 96])

# Make comparison crop
crop_b = img_before_result[180:680, 350:680]
crop_a = img_after[180:680, 350:680]
comp = np.hstack([crop_b, crop_a])
cv2.putText(comp, "PROPOSED NATURAL BEFORE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.putText(comp, "AFTER (FACIAL PAYOFF)", (350, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imwrite('scratch/comp_audit_stage1.jpg', comp)
print("Saved scratch/comp_audit_stage1.jpg")
