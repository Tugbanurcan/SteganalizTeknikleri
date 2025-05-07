import cv2
import numpy as np
import os

# Mesajı bitlere dönüştürür
def text_to_bits(text):
    text += "###"  # Mesajın sonu için belirteç
    return ''.join(format(ord(char), '08b') for char in text)

# Bitleri mesaja dönüştürür
def bits_to_text(bits):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    result = ''.join(chars)
    end_idx = result.find("###")
    return result[:end_idx] if end_idx != -1 else "Mesaj bulunamadı."

# Videoya mesaj gömme işlemi
def embed_message_to_video(input_path, output_path, message):
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakteri geçemez.")

    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(3))
    height = int(cap.get(4))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    binary_message = text_to_bits(message)
    bit_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if bit_idx < len(binary_message):
            # Pikselleri filteleme işlemi
            for row in frame:
                for pixel in row:
                    for i in range(3):  # B, G, R
                        if bit_idx < len(binary_message):
                            pixel[i] = (pixel[i] & ~1) | int(binary_message[bit_idx])
                            bit_idx += 1

        out.write(frame)

    cap.release()
    out.release()
    print(f"Mesaj başarıyla '{output_path}' dosyasına gizlendi.")

# Videodan mesaj çıkarma işlemi
def extract_message_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    bits = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Piksellerin maskeleme ile bilgilerini çıkarma
        for row in frame:
            for pixel in row:
                for i in range(3):  # B, G, R
                    bits += str(pixel[i] & 1)

    cap.release()
    message = bits_to_text(bits)
    print("Çözülen Mesaj:", message)

# Ana fonksiyon
def main():
    print("1. Mesajı videoya gizle")
    print("2. Videodan mesajı çıkar")
    secim = input("Seçiminiz (1/2): ")

    if secim == '1':
        input_video = 'bird.avi'
        if not os.path.exists(input_video):
            print("Video dosyası bulunamadı!")
            return
        message = input("Gizlenecek mesaj (maksimum 160 karakter): ")
        output_video = input("Çıkış video dosyası adı (örn: output.avi): ")
        embed_message_to_video(input_video, output_video, message)

    elif secim == '2':
        input_video = input("Gizli mesaj içeren video yolu: ")
        if not os.path.exists(input_video):
            print("Video dosyası bulunamadı!")
            return
        extract_message_from_video(input_video)

    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    main()
