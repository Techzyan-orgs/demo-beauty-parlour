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
    (L_orig >= 85) & (L_orig <= 245) &
    (A_orig >= 130) & (A_orig <= 160) &
    (B_orig >= 132) & (B_orig <= 170) &
    (r.astype(int) - b.astype(int) >= 22) &
    (g.astype(int) - b.astype(int) >= 6)
).astype(np.float32)

# Face spatial boundary polygon:
# Accurately enclosing forehead, cheeks, nose, mouth perimeter, chin, jawline:
face_poly = np.array([
    [460, 225], [510, 220], [555, 235], [580, 260],
    [610, 305], [630, 360], [640, 420], [638, 480],
    [620, 530], [585, 570], [550, 595], [510, 600],
    [470, 580], [450, 530], [440, 470], [442, 400],
    [448, 330], [452, 270]
], dtype=np.int32)

spatial_mask = np.zeros((h, w), dtype=np.float32)
cv2.fillPoly(spatial_mask, [face_poly], 1.0)
spatial_mask = cv2.GaussianBlur(spatial_mask, (21, 21), 0)

# Feature exclusions (eyeball openings, bindi, lips, earring):
feat_protect = np.zeros((h, w), dtype=np.float32)
# Eyeball left (viewer left): center (465, 355), r=(15, 8)
cv2.ellipse(feat_protect, (465, 355), (15, 8), -3, 0, 360, 1.0, -1)
# Eyeball right (viewer right): center (550, 352), r=(17, 9)
cv2.ellipse(feat_protect, (550, 352), (17, 9), 3, 0, 360, 1.0, -1)
# Bindi: center (491, 325), radius=6
cv2.circle(feat_protect, (491, 325), 6, 1.0, -1)
# Lips: center (495, 502), r=(32, 14)
cv2.ellipse(feat_protect, (495, 502), (32, 14), 1, 0, 360, 1.0, -1)
# Earring: center (655, 475), radius=28
cv2.circle(feat_protect, (655, 475), 28, 1.0, -1)

# Soft feathering on protection mask
feat_protect = cv2.GaussianBlur(feat_protect, (7, 7), 1.5)

# Full continuous weight mask for bare facial skin
w_skin = spatial_mask * is_skin_color * (1.0 - feat_protect)
w_skin = cv2.GaussianBlur(w_skin, (7, 7), 1.5)
w_skin = np.clip(w_skin, 0.0, 1.0)

# Strict outer boundary: anything outside bounding box or in hair/jewelry is 0
hard_zero = np.zeros((h, w), dtype=bool)
hard_zero[:200, :] = True
hard_zero[:, :430] = True
hard_zero[620:, :] = True
hard_zero[350:, 642:] = True  # Earring & flowers
w_skin[hard_zero] = 0.0

print(f"Skin mask max: {w_skin.max():.3f}, positive pixels: {np.sum(w_skin > 0.05)}")

# --- 2. SPECULAR HIGHLIGHT SUPPRESSION & MATTE/DULL COMPLEXION ---
L_work = L_orig.copy()
A_work = A_orig.copy()
B_work = B_orig.copy()

# Suppress cheekbone & nose specular highlight by 38%
spec_excess = np.maximum(0.0, L_orig - 142.0)
spec_zone = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(spec_zone, (600, 420), (40, 35), 15, 0, 360, 1.0, -1)
cv2.ellipse(spec_zone, (485, 390), (12, 35), -5, 0, 360, 0.8, -1)
spec_zone = cv2.GaussianBlur(spec_zone, (21, 21), 0)

# Base untreated skin dullness (L -11.0, B -2.2, A -0.5)
base_dullness = 11.0
L_work -= (base_dullness + spec_excess * 0.38 * spec_zone) * w_skin
B_work -= 2.2 * w_skin
A_work -= 0.5 * w_skin

# --- 3. KOLKATA SUN TAN / TONAL UNEVENNESS ---
tan_field = np.zeros((h, w), dtype=np.float32)
# Forehead tan: centered at (510, 265), axes (42, 22)
cv2.ellipse(tan_field, (510, 265), (42, 22), 0, 0, 360, 1.0, -1)
# Outer cheek / temple (viewer right): (610, 360), axes (25, 45), angle 10
cv2.ellipse(tan_field, (610, 360), (25, 45), 10, 0, 360, 0.9, -1)
# Outer cheek (viewer left): (455, 420), axes (15, 35), angle -10
cv2.ellipse(tan_field, (455, 420), (15, 35), -10, 0, 360, 0.8, -1)
tan_field = cv2.GaussianBlur(tan_field, (25, 25), 0)

# Tan modulation: L -16.0, dA +1.6, dB +3.2 (warm sun tan)
L_work -= 16.0 * tan_field * w_skin
A_work += 1.6 * tan_field * w_skin
B_work += 3.2 * tan_field * w_skin

# --- 4. UNDER-EYE DARK CIRCLES & FATIGUE ---
undereye_field = np.zeros((h, w), dtype=np.float32)
# Viewer left eye orbital hollow (465, 375)
cv2.ellipse(undereye_field, (465, 375), (16, 8), -3, 0, 360, 1.0, -1)
# Viewer right eye orbital hollow (550, 372)
cv2.ellipse(undereye_field, (550, 372), (18, 9), 3, 0, 360, 1.0, -1)
undereye_field = cv2.GaussianBlur(undereye_field, (11, 11), 0)

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
    (595, 415, 3.2, -32.0, 2.8, 4.8, 401),
    # 2. Apple of cheek blemish mark (viewer right)
    (548, 438, 2.8, -30.0, 2.6, 4.4, 402),
    # 3. Lower cheek mark (viewer right)
    (570, 462, 2.6, -28.0, 2.4, 4.0, 403),
    # 4. Temple sun speck (viewer right)
    (595, 345, 2.5, -29.0, 2.5, 4.2, 404),
    # 5. Flank of nose freckle (viewer right)
    (505, 412, 2.4, -28.0, 2.4, 4.0, 405),
    # 6. Forehead sun spot 1 (center-right)
    (525, 255, 3.0, -31.0, 2.8, 4.6, 406),
    # 7. Forehead sun spot 2 (center-left)
    (490, 268, 2.6, -28.0, 2.4, 4.2, 407),
    # 8. Forehead sun spot 3 (upper)
    (540, 248, 2.5, -28.0, 2.4, 4.0, 408),
    # 9. Viewer left cheek blemish mark
    (465, 428, 3.0, -31.0, 2.7, 4.5, 409),
    # 10. Viewer left lower cheek mark
    (460, 455, 2.5, -28.0, 2.4, 4.0, 410),
    # 11. Chin / Jawline authentic mark
    (535, 545, 3.0, -31.0, 2.8, 4.6, 411),
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

# Ensure spots are applied directly where w_skin is active
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
crop_b = out_img[180:680, 420:680]
crop_a = img_after[180:680, 420:680]
comp = np.hstack([crop_b, crop_a])
cv2.putText(comp, "BEFORE (UNTREATED SKIN)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
cv2.putText(comp, "AFTER (24K GOLD FACIAL)", (280, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
cv2.imwrite('scratch/comp_audit_stage1.jpg', comp)

# Verification checks
diff = np.abs(out_img.astype(int) - img_after.astype(int))
print(f"Total changed pixels: {np.sum(np.any(diff > 0, axis=2))}")
print(f"Outside zone max diff: {diff[hard_zero].max()} (MUST BE 0)")
print(f"Forehead diff max: {diff[240:280, 480:540].max()}")
print(f"Under-eye diff max: {diff[365:380, 535:565].max()}")
print(f"Cheek spot diff max: {diff[410:425, 590:605].max()}")
print("Successfully wrote public/images/trans-hair-before.jpg and scratch/comp_audit_stage1.jpg")
