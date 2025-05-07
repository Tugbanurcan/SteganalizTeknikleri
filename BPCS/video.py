import cv2
import numpy as np

# Video ayarları
width, height = 640, 480
fps = 24
frame_count = 100

# MJPG codec'iyle VideoWriter nesnesi
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('ornek.mp4', fourcc, fps, (width, height))

# Her biri siyah olan 100 kare üret
for _ in range(frame_count):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    out.write(frame)

out.release()
print("Test videosu 'ornek.mp4' oluşturuldu.")
