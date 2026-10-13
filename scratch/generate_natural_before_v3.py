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
# We want changes ONLY on bare facial skin.
# Background, hair, mogra flowers, saree, gold jewelry, bindi, lips, and eyes must remain 100% bit-exact (diff = 0).

# Feature exclusion masks:
# Eyes:
# Left eye (viewer left): center (413, 356), r=(22, 13)
# Right eye (viewer right): center (527, 352), r=(25, 14)
# Eyebrows:
# Left brow: center (405, 312), r=(32, 10), angle=-10
# Right brow: center (535, 305), r=(38, 12), angle=10
# Bindi: center (457, 312), radius=7
# Lips: center (455, 508), r=(42, 18)
# Earring: center (655, 475), radius=28
# Nostril cavities: (440, 435), (465, 435), radius=6

feat_protect = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(feat_protect, (413, 356), (22, 14), -5, 0, 360, 1.0, -1)
cv2.ellipse(feat_protect, (527, 352), (26, 15), 5, 0, 360, 1.0, -1)
cv2.ellipse(feat_protect, (405, 312), (34, 11), -10, 0, 360, 1.0, -1)
cv2.ellipse(feat_protect, (535, 305), (40, 12), 10, 0, 360, 1.0, -1)
cv2.circle(feat_protect, (457, 312), 8, 1.0, -1)
cv2.ellipse(feat_protect, (455, 508), (44, 20), 2, 0, 360, 1.0, -1)
cv2.circle(feat_protect, (655, 475), 28, 1.0, -1)
cv2.circle(feat_protect, (440, 435), 7, 1.0, -1)
cv2.circle(feat_protect, (465, 435), 7, 1.0, -1)

# Soft feathering on protection mask: sigma = 3
feat_protect = cv2.GaussianBlur(feat_protect, (11, 11), 2.5)

# Facial skin spatial boundary:
# Forehead, cheeks, nose, chin, upper neck
face_poly = np.array([
    [380, 215], [440, 205], [500, 215], [540, 245],
    [575, 285], [605, 340], [625, 400], [630, 470],
    [615, 520], [580, 560], [555, 600], [535, 650],
    [455, 650], [430, 600], [395, 550], [365, 500],
    [355, 440], [360, 370], [365, 300]
], dtype=np.int32)

face_spatial = np.zeros((h, w), dtype=np.float32)
cv2.fillPoly(face_spatial, [face_poly], 1.0)
# Smooth spatial boundary
face_spatial = cv2.GaussianBlur(face_spatial, (31, 31), 0)

# Skin color gate:
skin_color = (
    (L_orig >= 75) & (L_orig <= 245) &
    (A_orig >= 132) & (A_orig <= 162) &
    (B_orig >= 133) & (B_orig <= 172)
).astype(np.float32)
skin_color = cv2.GaussianBlur(skin_color, (7, 7), 0)

# Combine:
w_skin = face_spatial * skin_color * (1.0 - feat_protect)
w_skin = np.clip(w_skin, 0.0, 1.0)

# Absolute non-skin mask (outside face bounding box or hair):
outside_zone = np.zeros((h, w), dtype=bool)
outside_zone[:190, :] = True
outside_zone[:, :340] = True
outside_zone[670:, :] = True
outside_zone[370:, 640:] = True  # Earring & flowers
w_skin[outside_zone] = 0.0

print(f"w_skin min: {w_skin.min():.3f}, max: {w_skin.max():.3f}")

# Start with copies of original channels
L_new = L_orig.copy()
A_new = A_orig.copy()
B_new = B_orig.copy()

# --- 2. SPECULAR HIGHLIGHT SUPPRESSION & MATTE/DULL COMPLEXION ---
# The pristine After has high-specular glass-skin reflection on cheekbone (x: 560..625, y: 390..450) and nose.
# Suppress specular highlight by ~35%
spec_excess = np.maximum(0.0, L_orig - 145.0)
spec_mask = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(spec_mask, (585, 415), (45, 35), 15, 0, 360, 1.0, -1)
cv2.ellipse(spec_mask, (455, 390), (14, 35), -5, 0, 360, 0.8, -1)
spec_mask = cv2.GaussianBlur(spec_mask, (25, 25), 0)

# Natural bare skin dullness: untreated skin has ~9-11 less luminance than freshly treated 24K gold facial skin
base_dullness = 10.0
L_new -= (base_dullness + spec_excess * 0.35 * spec_mask) * w_skin
# Tone down the polished golden sheen (B -2.0, A -0.4)
B_new -= 2.0 * w_skin
A_new -= 0.4 * w_skin

# --- 3. KOLKATA SUN TAN / TONAL UNEVENNESS ---
# Kolkata climate causes tanning on forehead and cheek perimeters.
# Forehead tan: centered at (450, 245), axes (55, 26)
# Cheek perimeter / temple tan: (595, 370), axes (30, 55), angle 10
# Viewer left cheek tan: (380, 420), axes (20, 38), angle -10
tan_field = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(tan_field, (450, 245), (55, 26), 0, 0, 360, 1.0, -1)
cv2.ellipse(tan_field, (595, 370), (30, 55), 10, 0, 360, 0.9, -1)
cv2.ellipse(tan_field, (380, 420), (20, 38), -10, 0, 360, 0.7, -1)
tan_field = cv2.GaussianBlur(tan_field, (35, 35), 0)

# Tanning modulation: L -16.0, dA +1.5, dB +2.8 (melanin warmth)
L_new -= 16.0 * tan_field * w_skin
A_new += 1.5 * tan_field * w_skin
B_new += 2.8 * tan_field * w_skin

# --- 4. UNDER-EYE DARK CIRCLES & FATIGUE ---
# Lower orbital hollow under both eyes:
undereye_field = np.zeros((h, w), dtype=np.float32)
# Viewer left eye orbital hollow (415, 377)
cv2.ellipse(undereye_field, (415, 377), (20, 9), -5, 0, 360, 1.0, -1)
# Viewer right eye orbital hollow (530, 374)
cv2.ellipse(undereye_field, (530, 374), (22, 10), 5, 0, 360, 1.0, -1)
undereye_field = cv2.GaussianBlur(undereye_field, (13, 13), 0)

# Attenuation: L -18.0, dA +1.6, dB +0.5
L_new -= 18.0 * undereye_field * w_skin
A_new += 1.6 * undereye_field * w_skin
B_new += 0.5 * undereye_field * w_skin

# --- 5. NOTICEABLE NATURAL SUN SPOTS & BLEMISHES ---
# Function to generate organic melanin spot
def make_spot(radius, dL, dA, dB, rng_seed):
    np.random.seed(rng_seed)
    k_size = max(11, int(round(radius * 4)) | 1)
    cx, cy = k_size // 2, k_size // 2
    kernel = np.zeros((k_size, k_size), dtype=np.float32)
    
    r_maj = radius * np.random.uniform(0.9, 1.25)
    r_min = radius * np.random.uniform(0.7, 0.95)
    ang = np.random.uniform(0, 180)
    cv2.ellipse(kernel, (cx, cy), (int(round(r_maj)), int(round(r_min))), ang, 0, 360, 1.0, -1)
    
    # Secondary micro-lobe
    ox = int(round(np.random.uniform(-0.4, 0.4) * radius))
    oy = int(round(np.random.uniform(-0.4, 0.4) * radius))
    cv2.circle(kernel, (cx + ox, cy + oy), int(round(radius * 0.55)), 0.8, -1)
    
    # Soft Gaussian feathering preserving texture
    feather = cv2.GaussianBlur(kernel, (5, 5), 1.2)
    if feather.max() > 0:
        feather /= feather.max()
    return feather, cx, cy

# Distinct, authentic blemish marks & sun spots (clearly visible at normal web view!):
# Coordinates verified against grid_coords.jpg:
# 1. High cheekbone sun spot (viewer right): (578, 415), radius 3.0
# 2. Apple of cheek blemish mark (viewer right): (545, 438), radius 2.8
# 3. Mid cheek freckle (viewer right): (565, 460), radius 2.6
# 4. Temple sun speck (viewer right): (588, 348), radius 2.5
# 5. Forehead sun spot 1: (470, 245), radius 3.0
# 6. Forehead sun spot 2: (435, 258), radius 2.6
# 7. Viewer left cheek blemish mark: (390, 428), radius 3.0
# 8. Viewer left lower cheek: (382, 458), radius 2.5
# 9. Flank of nose freckle: (480, 412), radius 2.4
# 10. Jawline beauty mark: (518, 538), radius 3.0

blemish_list = [
    (578, 415, 3.0, -32.0, 2.8, 4.5, 201),
    (545, 438, 2.8, -30.0, 2.6, 4.2, 202),
    (565, 460, 2.6, -28.0, 2.4, 4.0, 203),
    (588, 348, 2.5, -29.0, 2.5, 4.2, 204),
    (470, 245, 3.0, -32.0, 2.8, 4.6, 205),
    (435, 258, 2.6, -28.0, 2.4, 4.0, 206),
    (390, 428, 3.0, -31.0, 2.7, 4.4, 207),
    (382, 458, 2.5, -28.0, 2.4, 4.0, 208),
    (480, 412, 2.4, -28.0, 2.4, 4.0, 209),
    (518, 538, 3.0, -32.0, 2.8, 4.6, 210),
]

spots_delta_L = np.zeros((h, w), dtype=np.float32)
spots_delta_A = np.zeros((h, w), dtype=np.float32)
spots_delta_B = np.zeros((h, w), dtype=np.float32)

for sx, sy, rad, dL, dA, dB, seed in blemish_list:
    patch, cx, cy = make_spot(rad, dL, dA, dB, seed)
    ph, pw = patch.shape
    y1, y2 = sy - cy, sy - cy + ph
    x1, x2 = sx - cx, sx - cx + pw
    spots_delta_L[y1:y2, x1:x2] += patch * dL
    spots_delta_A[y1:y2, x1:x2] += patch * dA
    spots_delta_B[y1:y2, x1:x2] += patch * dB

# Notice: apply spots directly on skin where w_skin > 0.3 without double-attenuation
spot_gate = np.clip(w_skin * 1.5, 0.0, 1.0)
L_new += spots_delta_L * spot_gate
A_new += spots_delta_A * spot_gate
B_new += spots_delta_B * spot_gate

# Clip LAB channels
L_out = np.clip(L_new, 0.0, 255.0)
A_out = np.clip(A_new, 0.0, 255.0)
B_out = np.clip(B_new, 0.0, 255.0)

lab_final = np.stack([L_out, A_out, B_out], axis=2).astype(np.uint8)
bgr_final = cv2.cvtColor(lab_final, cv2.COLOR_LAB2BGR)

# Seamless blend using w_skin:
# Where w_skin == 0, result is 100% bit-exact to img_after!
w_skin_3c = np.repeat(w_skin[:, :, np.newaxis], 3, axis=2)
result_img = np.round(
    img_after.astype(np.float32) * (1.0 - w_skin_3c) +
    bgr_final.astype(np.float32) * w_skin_3c
).clip(0, 255).astype(np.uint8)

# Guarantee 100% bit-exact non-skin preservation:
result_img[w_skin == 0.0] = img_after[w_skin == 0.0]
result_img[outside_zone] = img_after[outside_zone]
result_img[feat_protect > 0.5] = img_after[feat_protect > 0.5]

# Audit diff
diff_matrix = np.abs(result_img.astype(int) - img_after.astype(int))
total_diff_pixels = np.sum(np.any(diff_matrix > 0, axis=2))
print(f"Total modified skin pixels: {total_diff_pixels}")
print(f"Diff in outside_zone: {diff_matrix[outside_zone].max()} (MUST BE 0)")
print(f"Diff in earring (center 655, 475): {diff_matrix[465:485, 645:665].max()} (MUST BE 0)")
print(f"Diff in left eye center: {diff_matrix[350:360, 410:420].max()} (MUST BE 0)")
print(f"Diff in right eye center: {diff_matrix[348:356, 522:532].max()} (MUST BE 0)")
print(f"Diff in bindi (457, 312): {diff_matrix[310:315, 455:460].max()} (MUST BE 0)")

# Save side-by-side comparison for audit
crop_b = result_img[180:680, 350:680]
crop_a = img_after[180:680, 350:680]
comp = np.hstack([crop_b, crop_a])
cv2.putText(comp, "BEFORE (AUTHENTIC UNTREATED)", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
cv2.putText(comp, "AFTER (24K GOLD FACIAL)", (350, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
cv2.imwrite('scratch/comp_audit_stage1.jpg', comp)

# Also write directly to public/images/trans-hair-before.jpg
cv2.imwrite('public/images/trans-hair-before.jpg', result_img, [cv2.IMWRITE_JPEG_QUALITY, 96])
print("Saved public/images/trans-hair-before.jpg and scratch/comp_audit_stage1.jpg")
