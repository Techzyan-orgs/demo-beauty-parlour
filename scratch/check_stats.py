import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
h, w, _ = img.shape

# Let's inspect pixel values around the cheek (560..620, 400..460)
cheek_patch = img[400:460, 560:620]
print(f"Cheek patch shape: {cheek_patch.shape}, mean BGR: {cheek_patch.mean(axis=(0,1))}")
lab_patch = cv2.cvtColor(cheek_patch, cv2.COLOR_BGR2LAB)
print(f"Cheek patch mean LAB: L={lab_patch[:,:,0].mean():.1f}, A={lab_patch[:,:,1].mean():.1f}, B={lab_patch[:,:,2].mean():.1f}")
