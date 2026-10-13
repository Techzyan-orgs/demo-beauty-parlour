import cv2
import numpy as np

# Load pristine After image
img_after = cv2.imread('public/images/trans-hair-after.jpg')
h, w, c = img_after.shape
print(f"Loaded image: {w}x{h}")

lab = cv2.cvtColor(img_after, cv2.COLOR_BGR2LAB).astype(np.float32)
L = lab[:, :, 0]
A = lab[:, :, 1]
B = lab[:, :, 2]

# Spatial region of face:
face_spatial = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(face_spatial, (510, 400), (145, 160), 10, 0, 360, 1.0, -1)
face_spatial = cv2.GaussianBlur(face_spatial, (35, 35), 0)

# Skin color gate:
skin_color_gate = (
    (A >= 132) & (A <= 158) & 
    (B >= 134) & (B <= 168)
).astype(np.float32)
skin_color_gate = cv2.GaussianBlur(skin_color_gate, (9, 9), 0)

w_skin = face_spatial * skin_color_gate

# Exclude eyes pupil/iris core and earring
cv2.ellipse(w_skin, (460, 355), (18, 12), -5, 0, 360, 0, -1)
cv2.ellipse(w_skin, (550, 350), (22, 12), 5, 0, 360, 0, -1)
cv2.circle(w_skin, (697, 423), 22, 0, -1)
w_skin = cv2.GaussianBlur(w_skin, (7, 7), 0)

L_before = L.copy()
A_before = A.copy()
B_before = B.copy()

# 1. De-glaze specular highlights across face (turn dewy glass-skin into matte bare skin)
spec_excess = np.maximum(0.0, L - 138.0)
spec_reduction = spec_excess * 0.42 * w_skin

# Base skin dullness: -11.0 in LAB (natural untreated bare skin)
base_dullness = 11.0 * w_skin
L_before = L_before - (base_dullness + spec_reduction)

# Bare skin has less warm golden glow (B -2.2, A -0.5)
B_before = B_before - w_skin * 2.2
A_before = A_before - w_skin * 0.5

# 2. Soft Under-Eye Fatigue (Natural pre-wedding dark circles)
undereye = np.zeros((h, w), dtype=np.float32)
cv2.ellipse(undereye, (460, 375), (18, 10), -5, 0, 360, 0.8, -1)
cv2.ellipse(undereye, (550, 372), (24, 12), 5, 0, 360, 0.8, -1)
undereye = cv2.GaussianBlur(undereye, (15, 15), 0) * w_skin
L_before = L_before + undereye * (-11.0)
B_before = B_before + undereye * 1.6

# 3. Authentic Melanin Sun Freckles & Natural Skin Blemishes (warm brown, organic soft edges, ZERO black ink)
spots_L = np.zeros((h, w), dtype=np.float32)
spots_A = np.zeros((h, w), dtype=np.float32)
spots_B = np.zeros((h, w), dtype=np.float32)

freckles = [
    # (x, y, radius, dL, dA, dB)
    # Right cheek cluster (viewer left)
    (476, 432, 2.5, -20.0, 1.8, 3.2), # Right cheek sun freckle
    (483, 441, 1.8, -15.0, 1.4, 2.5), # Secondary micro-freckle
    # Left cheek / high cheekbone (viewer right)
    (564, 442, 2.8, -21.0, 1.8, 3.4), # Left cheek sun spot / blemish
    (574, 456, 2.0, -16.0, 1.4, 2.8), # Secondary cheek pigment mark
    (554, 468, 1.8, -14.0, 1.2, 2.2), # Lower cheek speck
    # Temple / upper cheek
    (588, 378, 2.4, -18.0, 1.5, 2.8), # Temple sun speck
    # Bridge and flank of nose
    (470, 405, 2.0, -16.0, 1.4, 2.5), # Bridge sun freckle
    (435, 435, 1.8, -15.0, 1.3, 2.2), # Nose flank speck
    # Jawline natural beauty mark
    (515, 525, 2.4, -20.0, 1.8, 3.2), # Natural jawline beauty mark
]

for sx, sy, srad, dL, dA, dB in freckles:
    sm = np.zeros((h, w), dtype=np.float32)
    cv2.circle(sm, (int(sx), int(sy)), int(round(srad)), 1.0, -1)
    sm = cv2.GaussianBlur(sm, (5, 5), 1.0)
    spots_L += sm * dL
    spots_A += sm * dA
    spots_B += sm * dB

L_before = np.clip(L_before + spots_L * w_skin, 0.0, 255.0)
A_before = np.clip(A_before + spots_A * w_skin, 0.0, 255.0)
B_before = np.clip(B_before + spots_B * w_skin, 0.0, 255.0)

lab_mod = np.stack([L_before, A_before, B_before], axis=2).astype(np.uint8)
bgr_mod = cv2.cvtColor(lab_mod, cv2.COLOR_LAB2BGR)

# Composite final image
w_skin_3c = np.repeat(w_skin[:, :, np.newaxis], 3, axis=2)
img_before_final = np.clip(
    img_after.astype(np.float32) * (1.0 - w_skin_3c) + 
    bgr_mod.astype(np.float32) * w_skin_3c,
    0, 255
).astype(np.uint8)

# Strict protection: ensure outside face is untouched
protected_zone = np.zeros((h, w), dtype=bool)
protected_zone[:200, :] = True
protected_zone[:, :340] = True
protected_zone[770:, :] = True
protected_zone[380:, 680:] = True
img_before_final[protected_zone] = img_after[protected_zone]

# Save directly to public/images/trans-hair-before.jpg
out_path = 'public/images/trans-hair-before.jpg'
cv2.imwrite(out_path, img_before_final, [cv2.IMWRITE_JPEG_QUALITY, 96])
print(f"Successfully wrote {out_path}")
