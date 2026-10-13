import cv2
import numpy as np

img = cv2.imread('public/images/trans-hair-after.jpg')
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

regions = {
    'Forehead (460, 250)': lab[245:255, 455:465],
    'Under-eye left (415, 375)': lab[372:378, 410:420],
    'Under-eye right (530, 372)': lab[369:375, 525:535],
    'Cheek highlight (585, 415)': lab[410:420, 580:590],
    'Cheek apple (545, 435)': lab[430:440, 540:550],
    'Chin (455, 575)': lab[570:580, 450:460],
    'Jawline (520, 540)': lab[535:545, 515:525],
    'Lips (455, 510)': lab[505:515, 450:460],
    'Left pupil (413, 356)': lab[354:358, 411:415],
    'Bindi (457, 312)': lab[310:314, 455:459],
}

for name, r in regions.items():
    L = r[:,:,0].mean()
    A = r[:,:,1].mean()
    B = r[:,:,2].mean()
    print(f"{name:30s} -> L={L:5.1f}, A={A:5.1f}, B={B:5.1f}")
