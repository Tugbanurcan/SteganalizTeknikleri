import wave
import os

# Mesajı ses dosyasına gizleyen fonksiyon
def embed_message(input_audio_path, output_audio_path, message):
    if len(message) > 160:
        raise ValueError("Mesaj 160 karakterden uzun olamaz.")

    message += '###'  # Mesajın bittiğini göstermek için özel işaret

    # Mesajı binary formatına çevir
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Ses dosyasını oku
    with wave.open(input_audio_path, 'rb') as audio:
        params = audio.getparams()
        frames = bytearray(audio.readframes(audio.getnframes()))

    # Mesajı LSB yöntemiyle gizle
    if len(binary_message) > len(frames):
        raise ValueError("Ses dosyası mesajı gizlemek için yeterli uzunlukta değil.")

    for i in range(len(binary_message)):
        frames[i] = (frames[i] & 254) | int(binary_message[i])

    # Yeni dosyaya yaz
    with wave.open(output_audio_path, 'wb') as output_audio:
        output_audio.setparams(params)
        output_audio.writeframes(frames)

    print(f"Mesaj başarıyla '{output_audio_path}' dosyasına gizlendi.")

# Gizlenmiş mesajı ses dosyasından çıkaran fonksiyon
def extract_message(stego_audio_path):
    with wave.open(stego_audio_path, 'rb') as audio:
        frames = bytearray(audio.readframes(audio.getnframes()))

    bits = [str(frames[i] & 1) for i in range(len(frames))]
    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]

    message = ''.join(chars)
    end_marker = message.find('###')
    if end_marker != -1:
        print("Çözülen Mesaj:", message[:end_marker])
    else:
        print("Mesaj bulunamadı.")

# Ana kontrol fonksiyonu
def main():
    print("1. Mesaj gizle")
    print("2. Mesaj çıkar")
    secim = input("Seçiminizi yapın (1/2): ")

    if secim == '1':
        input_audio = 'ornek.wav'
        if not os.path.exists(input_audio):
            print("Ses dosyası bulunamadı!")
            return
        message = input("Gizlenecek mesajı girin (en fazla 160 karakter): ")
        output_audio = input("Çıkış WAV dosyası adı (örn: output.wav): ")
        embed_message(input_audio, output_audio, message)

    elif secim == '2':
        stego_audio = input("Gizli mesaj içeren WAV dosyası yolunu girin: ")
        if not os.path.exists(stego_audio):
            print("Ses dosyası bulunamadı!")
            return
        extract_message(stego_audio)

    else:
        print("Geçersiz seçim.")

if __name__ == "__main__":
    main()
