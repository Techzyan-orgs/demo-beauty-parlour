import cv2
import numpy as np

img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img_after.shape

lab_after = cv2.cvtColor(img_after, cv2.COLOR_BGR2LAB).astype(np.float32)
L_orig = lab_after[:, :, 0]
A_orig = lab_after[:, :, 1]
B_orig = lab_after[:, :, 2]

# --- 1. CONTINUOUS SKIN WEIGHT MASK ---
b, g, r = cv2.split(img_after)
is_skin_color = (
    (L_orig >= 85) & (L_orig <= 245) &
    (A_orig >= 130) & (A_orig <= 160) &
    (B_orig >= 132) & (B_orig <= 170) &
    (r.astype(int) - b.astype(int) >= 20) &
    (g.astype(int) - b.astype(int) >= 5)
).astype(np.float32)

face_poly = np.array([
    [460, 225], [510, 220], [555, 235], [580, 260],
    [610, 305], [630, 360], [640, 420], [638, 480],
    [620, 530], [585, 570], [550, 595], [510, 600],
    [470, 580], [450, 530], [440, 470], [442, 400],
    [448, 330], [452, 270]
], dtype=np.int32)

spatial_mask = np.zeros((h, w), dtype=np.float32)
cv2.fillPoly(spatial_mask, [face_poly], 1.0)
spatial_mask = cv2.GaussianBlur(spatial_mask, (25, 25), 0)

# Feature exclusions (eyeballs, bindi, lips, earring):
feat_protect = np.zeros((h, w), dtype=np.float32)
# Eyeball left (viewer left): center (465, 355), r=(14, 7)
cv2.ellipse(feat_protect, (465, 355), (14, 7), -3, 0, 360, 1.0, -1)
# Eyeball right (viewer right): center (550, 352), r=(16, 8)
cv2.ellipse(feat_protect, (550, 352), (16, 8), 3, 0, 360, 1.0, -1)
# Bindi
cv2.circle(feat_protect, (491, 325), 6, 1.0, -1)
# Lips
cv2.ellipse(feat_protect, (495, 502), (30, 13), 1, 0, 360, 1.0, -1)
# Earring
cv2.circle(feat_protect, (655, 475), 28, 1.0, -1)
feat_protect = cv2.GaussianBlur(feat_protect, (7, 7), 1.5)

w_skin = spatial_mask * is_skin_color * (1.0 - feat_protect)
w_skin = cv2.GaussianBlur(w_skin, (7, 7), 1.5)
w_skin = np.clip(w_skin, 0.0, 1.0)

hard_zero = np.zeros((h, w), dtype=bool)
hard_zero[:200, :] = True
hard_zero[:, :430] = True
hard_zero[620:, :] = True
hard_zero[350:, 642:] = True
w_skin[hard_zero] = 0.0

L_work = L_orig.copy()
A_work = A_orig.copy()
B_work = B_orig.copy()

# --- 2. MATTE & DULL DEHYDRATED COMPLEXION (SUPPRESS GLASS-SKIN SHEEN) ---
# Suppress the bright specular reflection on cheekbone & nose by 35%
spec_zone = np.zeros((h, w), dtype=np.float32)
# Cheekbone specular highlight
cv2.ellipse(spec_zone, (595, 415), (45, 35), 15, 0, 360, 1.0, -1)
# Nose bridge specular highlight
cv2.ellipse(spec_zone, (485, 385), (12, 35), -5, 0, 360, 0.8, -1)
spec_zone = cv2.GaussianBlur(spec_zone, (25, 25), 0)

# Highlight reduction: where L > 145, reduce by 35% of excess
spec_excess = np.maximum(0.0, L_orig - 145.0)
L_work -= (spec_excess * 0.35 * spec_zone) * w_skin

# Base untreated skin dullness: L -8.0 across bare skin
# Untreated skin maintains natural warm caramel tone, so B slightly increases (+0.5)
L_work -= 8.0 * w_skin
B_work += 0.5 * w_skin

# --- 3. KOLKATA SUN TAN / TONAL UNEVENNESS ---
# Forehead tan & perimeter cheek tan: deeper caramel tan (L -14.0, dA +1.4, dB +3.0)
tan_field = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(tan_field, (515, 260), (40, 20), 0, 0, 360, 1.0, -1)
cv2.ellipse(tan_field, (610, 365), (22, 45), 10, 0, 360, 0.85, -1)
cv2.ellipse(tan_field, (455, 420), (14, 30), -10, 0, 360, 0.75, -1)
tan_field = cv2.GaussianBlur(tan_field, (27, 27), 0)

L_work -= 14.0 * tan_field * w_skin
A_work += 1.4 * tan_field * w_skin
B_work += 3.0 * tan_field * w_skin

# --- 4. UNDER-EYE DARK CIRCLES & FATIGUE ---
# Orbital hollow tiredness: L -16.0, dA +1.4, dB +1.0
undereye_field = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(undereye_field, (465, 373), (16, 8), -3, 0, 360, 1.0, -1)
cv2.ellipse(undereye_field, (550, 370), (18, 9), 3, 0, 360, 1.0, -1)
undereye_field = cv2.GaussianBlur(undereye_field, (11, 11), 0)

L_work -= 16.0 * undereye_field * w_skin
A_work += 1.4 * undereye_field * w_skin
B_work += 1.0 * undereye_field * w_skin

# --- 5. AUTHENTIC SUN SPOTS & ACNE BLEMISH MARKS ---
def make_organic_spot(radius, dL, dA, dB, rng_seed):
    np.random.seed(rng_seed)
    k_size = max(11, int(round(radius * 4)) | 1)
    cx, cy = k_size // 2, k_size // 2
    kernel = np.zeros((k_size, k_size), dtype=np.float32)
    
    # Asymmetric ellipse
    r_maj = radius * np.random.uniform(0.95, 1.25)
    r_min = radius * np.random.uniform(0.75, 0.95)
    ang = np.random.uniform(0, 180)
    cv2.ellipse(kernel, (cx, cy), (int(round(r_maj)), int(round(r_min))), ang, 0, 360, 1.0, -1)
    
    # Small secondary protrusion
    ox = int(round(np.random.uniform(-0.35, 0.35) * radius))
    oy = int(round(np.random.uniform(-0.35, 0.35) * radius))
    cv2.circle(kernel, (cx + ox, cy + oy), max(1, int(round(radius * 0.55))), 0.85, -1)
    
    feather = cv2.GaussianBlur(kernel, (5, 5), 1.1)
    if feather.max() > 0:
        feather /= feather.max()
    return feather, cx, cy

# Distinct, authentic melanin spots across all key zones:
# Sizes 2.5 to 3.2px radius (5 to 6.5px diameter)
# Melanin colors: dL -28 to -33, dA +2.5 to +3.0, dB +4.2 to +5.0
blemishes = [
    # 1. High cheekbone sun spot (viewer right) - clearly visible
    (590, 412, 3.0, -32.0, 2.8, 4.8, 601),
    # 2. Apple of cheek blemish mark (viewer right)
    (550, 436, 2.8, -30.0, 2.6, 4.5, 602),
    # 3. Lower cheek pigment mark (viewer right)
    (570, 465, 2.6, -28.0, 2.4, 4.2, 603),
    # 4. Temple sun speck (viewer right)
    (600, 352, 2.5, -28.0, 2.5, 4.2, 604),
    # 5. Flank of nose freckle (viewer right)
    (504, 414, 2.5, -28.0, 2.5, 4.2, 605),
    # 6. Forehead sun spot 1 (center-right)
    (522, 260, 3.0, -31.0, 2.8, 4.8, 606),
    # 7. Forehead sun spot 2 (center-left)
    (492, 272, 2.7, -29.0, 2.6, 4.4, 607),
    # 8. Forehead sun spot 3 (upper forehead)
    (538, 248, 2.4, -27.0, 2.4, 4.0, 608),
    # 9. Viewer left cheek blemish mark
    (466, 424, 2.8, -30.0, 2.7, 4.6, 609),
    # 10. Viewer left lower cheek mark
    (460, 454, 2.5, -28.0, 2.4, 4.2, 610),
    # 11. Jawline natural mark
    (532, 548, 2.9, -31.0, 2.8, 4.8, 611),
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

# Ensure spots are applied directly on skin where w_skin is active
spot_gate = np.clip(w_skin * 2.5, 0.0, 1.0)
L_work += spots_L * spot_gate
A_work += spots_A * spot_gate
B_work += spots_B * spot_gate

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

# Strict non-skin preservation (diff = 0)
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
print(f"High cheekbone spot diff max: {diff[405:420, 585:595].max()}")
print(f"Forehead spot diff max: {diff[255:265, 515:525].max()}")
print("Successfully generated refined Before image!")
