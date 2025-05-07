import cv2
import numpy as np

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join([chr(int(c, 2)) for c in chars if len(c) == 8])

def is_complex(block):
    transitions = np.sum(block[:, :-1] != block[:, 1:]) + np.sum(block[:-1, :] != block[1:, :])
    return transitions > (block.size * 0.3)

def embed_message_bpcs(video_path, message, output_path):
    bits = text_to_bits(message)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(3))
    height = int(cap.get(4))
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'XVID'), fps, (width, height))

    bit_index = 0
    block_size = 8

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                if bit_index + 64 > len(bits):
                    break

                block = frame[y:y+block_size, x:x+block_size, 0]
                if block.shape[:2] != (block_size, block_size):
                    continue

                lsb_plane = block & 1
                if is_complex(lsb_plane):
                    data_block = np.array([[int(b) for b in bits[bit_index:bit_index+8]] for _ in range(8)], dtype=np.uint8)
                    frame[y:y+block_size, x:x+block_size, 0] &= np.uint8(254)  # LSB sıfırlanır
                    frame[y:y+block_size, x:x+block_size, 0] |= data_block    # Veri yazılır
                    bit_index += 64

        out.write(frame)
        if bit_index >= len(bits):
            break

    cap.release()
    out.release()
    print("Video'ya BPCS benzeri yöntemle mesaj gömüldü.")

def extract_message_bpcs(video_path, message_length):
    cap = cv2.VideoCapture(video_path)
    bits = ""
    block_size = 8
    needed_bits = message_length * 8

    while cap.isOpened() and len(bits) < needed_bits:
        ret, frame = cap.read()
        if not ret:
            break
        height, width = frame.shape[:2]

        for y in range(0, height, block_size):
            for x in range(0, width, block_size):
                if len(bits) + 64 > needed_bits:
                    break

                block = frame[y:y+block_size, x:x+block_size, 0]
                if block.shape[:2] != (block_size, block_size):
                    continue

                lsb_plane = block & 1
                if is_complex(lsb_plane):
                    bits += ''.join(str(b) for b in lsb_plane.flatten())

                if len(bits) >= needed_bits:
                    break
    cap.release()
    return bits_to_text(bits[:needed_bits])

# Kullanım
message = input("Gizlenecek mesaj (max 160 karakter): ")[:160]
embed_message_bpcs("ornek.mp4", message, "bpcs_stego.avi")
extracted = extract_message_bpcs("bpcs_stego.avi", len(message))
print("Çıkarılan mesaj:", extracted)
