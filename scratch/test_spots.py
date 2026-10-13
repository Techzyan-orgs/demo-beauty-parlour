import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img.shape

# Let's write a specialized spot generator function
def create_organic_spot(radius, dL, dA, dB, rng_seed=None):
    if rng_seed is not None:
        np.random.seed(rng_seed)
    # create a small kernel
    k_size = int(round(radius * 4)) | 1  # odd size
    k_size = max(9, k_size)
    cx, cy = k_size // 2, k_size // 2
    
    # Create irregular base shape by combining 2-3 overlapping ellipses
    kernel = np.zeros((k_size, k_size), dtype=np.float32)
    
    # primary ellipse
    r_major = radius * np.random.uniform(0.9, 1.2)
    r_minor = radius * np.random.uniform(0.7, 0.95)
    angle = np.random.uniform(0, 180)
    cv2.ellipse(kernel, (cx, cy), (int(round(r_major)), int(round(r_minor))), angle, 0, 360, 1.0, -1)
    
    # small satellite protrusion
    offset_x = int(round(np.random.uniform(-0.5, 0.5) * radius))
    offset_y = int(round(np.random.uniform(-0.5, 0.5) * radius))
    r_sub = radius * np.random.uniform(0.4, 0.7)
    cv2.circle(kernel, (cx + offset_x, cy + offset_y), int(round(r_sub)), 0.8, -1)
    
    # Feathering with Gaussian blur preserving organic gradient
    feathered = cv2.GaussianBlur(kernel, (5, 5), 1.2)
    if feathered.max() > 0:
        feathered = feathered / feathered.max()
        
    return feathered, cx, cy

# Let's test applying this to the cheek and inspect
test_img = img.copy()
lab = cv2.cvtColor(test_img, cv2.COLOR_BGR2LAB).astype(np.float32)

test_spots = [
    # (x, y, radius, dL, dA, dB, seed)
    (580, 420, 3.0, -32.0, 2.8, 4.5, 101),
    (545, 440, 2.8, -30.0, 2.5, 4.0, 102),
    (565, 465, 2.5, -28.0, 2.2, 3.8, 103),
    (595, 345, 2.6, -30.0, 2.5, 4.2, 104),
    (475, 250, 3.2, -32.0, 2.8, 4.5, 105),
    (425, 265, 2.5, -28.0, 2.4, 3.8, 106),
    (385, 435, 3.0, -30.0, 2.6, 4.2, 107),
    (480, 410, 2.4, -28.0, 2.3, 3.8, 108),
    (520, 540, 3.0, -32.0, 2.8, 4.5, 109),
]

for sx, sy, rad, dL, dA, dB, seed in test_spots:
    patch, cx, cy = create_organic_spot(rad, dL, dA, dB, seed)
    ph, pw = patch.shape
    y1, y2 = sy - cy, sy - cy + ph
    x1, x2 = sx - cx, sx - cx + pw
    
    # Additive modulation in LAB
    lab[y1:y2, x1:x2, 0] += patch * dL
    lab[y1:y2, x1:x2, 1] += patch * dA
    lab[y1:y2, x1:x2, 2] += patch * dB

lab = np.clip(lab, 0, 255).astype(np.uint8)
res = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

# Save both high-res crop of cheek and full face crop
cv2.imwrite('scratch/test_spot_cheek_zoom.jpg', res[390:480, 530:620])
cv2.imwrite('scratch/test_spot_face.jpg', res[180:680, 350:680])
print("Saved spot tests successfully")
