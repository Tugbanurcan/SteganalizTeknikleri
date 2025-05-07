import numpy as np
import scipy.io.wavfile as wav
import math

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits):
    chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def embed_bpcs(audio_path, message, output_path):
    rate, data = wav.read(audio_path)
    if data.ndim > 1:
        data = data[:, 0]  # Mono ses
    bits = text_to_bits(message)
    flat = data.flatten()
    
    for i in range(len(bits)):
        flat[i] = (flat[i] & ~1) | int(bits[i])
    
    wav.write(output_path, rate, flat.astype(np.int16))
    print("Mesaj başarıyla gömüldü!")

def extract_bpcs(stego_audio_path, length):
    rate, data = wav.read(stego_audio_path)
    if data.ndim > 1:
        data = data[:, 0]
    bits = ""
    for i in range(length * 8):
        bits += str(data[i] & 1)
    return bits_to_text(bits)

# Kullanım
message = input("Gizlenecek mesaj (en fazla 160 karakter): ")[:160]
embed_bpcs("ornek.wav", message, "stego_ornek.wav")
extracted = extract_bpcs("stego_ornek.wav", len(message))
print("Çıkarılan Mesaj:", extracted)
