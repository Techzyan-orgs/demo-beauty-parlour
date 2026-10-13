import cv2
import numpy as np

# Load pristine After image
img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img_after.shape
print(f"Loaded image: {w}x{h}")

lab_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2LAB).astype(np.float32)
L_orig = lab_after[:, :, 0]
A_orig = lab_after[:, :, 1]
B_orig = lab_after[:, :, 2]

# --- 1. PRECISE SEAMLESS SKIN MASK ---
b, g, r = cv2.split(img_after)
is_skin_color = (
    (L_orig >= 90) & (L_orig <= 245) &
    (A_orig >= 132) & (A_orig <= 158) &
    (B_orig >= 134) & (B_orig <= 168) &
    (r.astype(int) - b.astype(int) >= 28) &
    (g.astype(int) - b.astype(int) >= 8)
).astype(np.float32)

# Face spatial boundary polygon:
face_poly = np.array([
    [365, 215], [410, 210], [455, 220], [480, 240],
    [520, 265], [560, 290], [590, 330], [615, 380],
    [628, 440], [625, 490], [610, 530], [580, 560],
    [545, 580], [510, 600], [450, 600], [410, 570],
    [375, 520], [355, 450], [350, 370], [355, 290]
], dtype=np.int32)

spatial_mask = np.zeros((h, w), dtype=np.float32)
cv2.fillPoly(spatial_mask, [face_poly], 1.0)
spatial_mask = cv2.GaussianBlur(spatial_mask, (25, 25), 0)

# Feature exclusions (only eyeball openings, bindi, lips, earring):
feat_protect = np.zeros((h, w), dtype=np.float32)
# Eyeball left (viewer left): x: 398..430, y: 348..365
cv2.ellipse(feat_protect, (414, 356), (16, 8), -5, 0, 360, 1.0, -1)
# Eyeball right (viewer right): x: 508..548, y: 344..362
cv2.ellipse(feat_protect, (528, 353), (19, 9), 5, 0, 360, 1.0, -1)
# Bindi
cv2.circle(feat_protect, (468, 312), 6, 1.0, -1)
# Lips
cv2.ellipse(feat_protect, (455, 508), (38, 16), 2, 0, 360, 1.0, -1)
# Earring
cv2.circle(feat_protect, (655, 475), 26, 1.0, -1)

# Smooth feathering on protection mask
feat_protect = cv2.GaussianBlur(feat_protect, (7, 7), 1.5)

# Full continuous weight mask for bare facial skin
w_skin = spatial_mask * is_skin_color * (1.0 - feat_protect)
w_skin = cv2.GaussianBlur(w_skin, (7, 7), 1.5)
w_skin = np.clip(w_skin, 0.0, 1.0)

# Strict outer boundary: anything outside bounding box or in hair is 0
hard_zero = np.zeros((h, w), dtype=bool)
hard_zero[:195, :] = True
hard_zero[:, :340] = True
hard_zero[620:, :] = True
hard_zero[370:, 635:] = True  # Earring & flowers
w_skin[hard_zero] = 0.0

print(f"Skin mask max: {w_skin.max():.3f}, total positive: {np.sum(w_skin > 0.05)}")

# --- 2. DE-GLAZE SPECULAR HIGHLIGHTS & MATTE/DULL COMPLEXION ---
L_work = L_orig.copy()
A_work = A_orig.copy()
B_work = B_orig.copy()

# Suppress cheekbone & nose specular highlight by 35%
spec_excess = np.maximum(0.0, L_orig - 145.0)
spec_zone = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(spec_zone, (585, 415), (42, 35), 15, 0, 360, 1.0, -1)
cv2.ellipse(spec_zone, (455, 390), (12, 35), -5, 0, 360, 0.8, -1)
spec_zone = cv2.GaussianBlur(spec_zone, (21, 21), 0)

# Base untreated skin dullness (L -11.0, B -2.2, A -0.5)
base_dullness = 11.0
L_work -= (base_dullness + spec_excess * 0.38 * spec_zone) * w_skin
B_work -= 2.2 * w_skin
A_work -= 0.5 * w_skin

# --- 3. KOLKATA SUN TAN / TONAL UNEVENNESS ---
# Forehead tan & perimeter cheek tan
tan_field = np.zeros((h, w), dtype=np.float32)
# Forehead: center (415, 260), axes (42, 24)
cv2.ellipse(tan_field, (415, 260), (42, 24), 0, 0, 360, 1.0, -1)
# Outer cheek / temple (viewer right): (595, 365), axes (28, 50), angle 10
cv2.ellipse(tan_field, (595, 365), (28, 50), 10, 0, 360, 0.9, -1)
# Outer cheek (viewer left): (375, 420), axes (18, 35), angle -10
cv2.ellipse(tan_field, (375, 420), (18, 35), -10, 0, 360, 0.8, -1)
tan_field = cv2.GaussianBlur(tan_field, (29, 29), 0)

# Tan modulation: L -16.0, dA +1.6, dB +3.2 (warm sun tan)
L_work -= 16.0 * tan_field * w_skin
A_work += 1.6 * tan_field * w_skin
B_work += 3.2 * tan_field * w_skin

# --- 4. UNDER-EYE DARK CIRCLES & FATIGUE ---
undereye_field = np.zeros((h, w), dtype=np.float32)
# Viewer left eye orbital hollow (414, 374)
cv2.ellipse(undereye_field, (414, 374), (18, 9), -5, 0, 360, 1.0, -1)
# Viewer right eye orbital hollow (528, 370)
cv2.ellipse(undereye_field, (528, 370), (20, 10), 5, 0, 360, 1.0, -1)
undereye_field = cv2.GaussianBlur(undereye_field, (13, 13), 0)

# Dark circles modulation: L -18.0, dA +1.6, dB +0.5
L_work -= 18.0 * undereye_field * w_skin
A_work += 1.6 * undereye_field * w_skin
B_work += 0.5 * undereye_field * w_skin

# --- 5. AUTHENTIC SUN SPOTS & ACNE BLEMISH MARKS ---
def make_organic_spot(radius, dL, dA, dB, rng_seed):
    np.random.seed(rng_seed)
    k_size = max(11, int(round(radius * 4)) | 1)
    cx, cy = k_size // 2, k_size // 2
    kernel = np.zeros((k_size, k_size), dtype=np.float32)
    
    r_maj = radius * np.random.uniform(0.9, 1.2)
    r_min = radius * np.random.uniform(0.75, 0.95)
    ang = np.random.uniform(0, 180)
    cv2.ellipse(kernel, (cx, cy), (int(round(r_maj)), int(round(r_min))), ang, 0, 360, 1.0, -1)
    
    # Secondary micro-lobe for organic asymmetry
    ox = int(round(np.random.uniform(-0.4, 0.4) * radius))
    oy = int(round(np.random.uniform(-0.4, 0.4) * radius))
    cv2.circle(kernel, (cx + ox, cy + oy), max(1, int(round(radius * 0.5))), 0.85, -1)
    
    feather = cv2.GaussianBlur(kernel, (5, 5), 1.1)
    if feather.max() > 0:
        feather /= feather.max()
    return feather, cx, cy

blemishes = [
    # 1. High cheekbone sun spot (viewer right) - very prominent
    (580, 418, 3.2, -32.0, 2.8, 4.8, 301),
    # 2. Apple of cheek blemish mark (viewer right)
    (545, 436, 2.8, -30.0, 2.6, 4.4, 302),
    # 3. Lower cheek mark (viewer right)
    (565, 465, 2.6, -28.0, 2.4, 4.0, 303),
    # 4. Temple sun speck (viewer right)
    (592, 345, 2.5, -29.0, 2.5, 4.2, 304),
    # 5. Flank of nose freckle (viewer right)
    (482, 412, 2.4, -28.0, 2.4, 4.0, 305),
    # 6. Forehead sun spot 1 (viewer left/mid forehead)
    (415, 255, 3.0, -31.0, 2.8, 4.6, 306),
    # 7. Forehead sun spot 2
    (438, 272, 2.6, -28.0, 2.4, 4.2, 307),
    # 8. Forehead sun spot 3
    (392, 268, 2.4, -27.0, 2.3, 4.0, 308),
    # 9. Viewer left cheek blemish mark
    (385, 425, 3.0, -31.0, 2.7, 4.5, 309),
    # 10. Viewer left lower cheek mark
    (378, 455, 2.5, -28.0, 2.4, 4.0, 310),
    # 11. Jawline authentic mark
    (512, 538, 3.0, -31.0, 2.8, 4.6, 311),
]

spots_L = np.zeros((h, w), dtype=np.float32)
spots_A = np.zeros((h, w), dtype=np.float32)
spots_B = np.zeros((h, w), dtype=np.float32)

for sx, sy, rad, dL, dA, dB, seed in blemishes:
    patch, cx, cy = make_organic_spot(rad, dL, dA, dB, seed)
    ph, pw = patch.shape
    y1, y2 = sy - cy, sy - cy + ph
    x1, x2 = sx - cx, sx - cx + pw
    spots_L[y1:y2, x1:x2] += patch * dL
    spots_A[y1:y2, x1:x2] += patch * dA
    spots_B[y1:y2, x1:x2] += patch * dB

# Ensure spots are applied with high contrast where w_skin is active
spot_presence = np.clip(w_skin * 2.0, 0.0, 1.0)
L_work += spots_L * spot_presence
A_work += spots_A * spot_presence
B_work += spots_B * spot_presence

# Convert modified LAB back to BGR
L_clipped = np.clip(L_work, 0.0, 255.0)
A_clipped = np.clip(A_work, 0.0, 255.0)
B_clipped = np.clip(B_work, 0.0, 255.0)

lab_res = np.stack([L_clipped, A_clipped, B_clipped], axis=2).astype(np.uint8)
bgr_res = cv2.cvtColor(lab_res, cv2.COLOR_LAB2BGR)

# Seamless blend:
# For pixels where w_skin > 0, blend continuously.
# For pixels where w_skin == 0, strictly preserve img_after bit-exact!
w_skin_3c = np.repeat(w_skin[:, :, np.newaxis], 3, axis=2)
out_img = np.round(
    img_after.astype(np.float32) * (1.0 - w_skin_3c) +
    bgr_res.astype(np.float32) * w_skin_3c
).clip(0, 255).astype(np.uint8)

# Guarantee bit-exact preservation on non-skin:
out_img[w_skin == 0.0] = img_after[w_skin == 0.0]
out_img[hard_zero] = img_after[hard_zero]

# Save to public/images/trans-hair-before.jpg
cv2.imwrite('public/images/trans-hair-before.jpg', out_img, [cv2.IMWRITE_JPEG_QUALITY, 96])

# Make comparison crop
crop_b = out_img[180:680, 350:680]
crop_a = img_after[180:680, 350:680]
comp = np.hstack([crop_b, crop_a])
cv2.putText(comp, "BEFORE (UNTREATED SKIN)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
cv2.putText(comp, "AFTER (BRIDAL FACIAL)", (350, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
cv2.imwrite('scratch/comp_audit_stage1.jpg', comp)

# Verification checks
diff = np.abs(out_img.astype(int) - img_after.astype(int))
print(f"Total changed pixels: {np.sum(np.any(diff > 0, axis=2))}")
print(f"Outside zone max diff: {diff[hard_zero].max()} (MUST BE 0)")
print(f"Forehead diff max: {diff[230:280, 400:440].max()}")
print(f"Under-eye diff max: {diff[365:380, 515:545].max()}")
print(f"Cheek spot diff max: {diff[410:425, 575:585].max()}")
print("Successfully wrote public/images/trans-hair-before.jpg and scratch/comp_audit_stage1.jpg")
