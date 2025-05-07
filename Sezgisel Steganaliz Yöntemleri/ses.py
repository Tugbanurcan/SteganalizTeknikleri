import wave
import numpy as np

# Mesajı ses dosyasına gömme fonksiyonu
def hide_message_in_audio(audio_path, message, output_audio_path):
    # Ses dosyasını aç
    with wave.open(audio_path, 'rb') as audio_file:
        # Ses dosyasının parametrelerini al
        params = audio_file.getparams()
        frames = audio_file.readframes(params.nframes)
        
        # Mesajı bitlere çevir
        message_bin = ''.join(format(ord(i), '08b') for i in message) + '1111111111111110'  # Mesaj bitlerine ve sonlandırıcıya ekle
        message_len = len(message_bin)

        # Sesin her bir örneği için bitleri değiştirme
        audio_samples = np.frombuffer(frames, dtype=np.int16)
        
        # Yazılabilir bir kopyasını oluştur
        audio_samples = audio_samples.copy()

        # Mesajı sesin LSB'lerine gömme
        for i in range(message_len):
            audio_samples[i] = (audio_samples[i] & 0xFFFE) | int(message_bin[i])  # LSB'yi mesaj bitine set et

        # Yeni ses verisini yaz
        with wave.open(output_audio_path, 'wb') as output_file:
            output_file.setparams(params)
            output_file.writeframes(audio_samples.tobytes())
    print("Mesaj başarıyla ses dosyasına gömüldü.")

# Ses dosyasından mesaj çıkarma fonksiyonu
def extract_message_from_audio(audio_path):
    # Ses dosyasını aç
    with wave.open(audio_path, 'rb') as audio_file:
        # Ses dosyasının parametrelerini al
        params = audio_file.getparams()
        frames = audio_file.readframes(params.nframes)

        # Ses verilerini numpy dizisine dönüştür
        audio_samples = np.frombuffer(frames, dtype=np.int16)

        # LSB bitlerini al ve mesajı çöz
        message_bin = ''
        for sample in audio_samples:
            message_bin += str(sample & 1)  # LSB'yi al

        # Mesajı binariden ASCII'ye çevir
        message = ''
        for i in range(0, len(message_bin), 8):
            byte = message_bin[i:i+8]
            if len(byte) < 8:
                break
            char = chr(int(byte, 2))
            if char == '\u0000':  # Null karakter (sonlandırıcı)
                break
            message += char

    return message

# Ana fonksiyon
def main():
    input_audio = "h.wav"  # Girdi ses dosyası
    output_audio = "output_audio.wav"  # Çıkış ses dosyası
    secret_message = "helloo"  # Gömülecek gizli mesaj
    
    # Mesajı ses dosyasına gömme
    hide_message_in_audio(input_audio, secret_message, output_audio)

    # Yeni ses dosyasından mesajı çıkarma
    extracted_message = extract_message_from_audio(output_audio)
    print("Çıkarılan Mesaj:", extracted_message)

# Kodun çalıştırılması
if __name__ == "__main__":
    main()
