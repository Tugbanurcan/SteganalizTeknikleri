import wave

# Mesajı UTF-8 ile binary'ye çevir
def text_to_binary(text):
    return ''.join(f'{byte:08b}' for byte in text.encode('utf-8'))

# Binary'yi tekrar UTF-8 metne çevir
def binary_to_text(binary_str):
    bytes_list = [int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8)]
    return bytes(bytes_list).decode('utf-8', errors='ignore')

# Mesajı ses dosyasına göm
def embed_message(audio_in, audio_out, message):
    if len(message.encode('utf-8')) > 160:
        print("Hata: Mesaj 160 bayttan uzun! Daha kısa bir mesaj girin.")
        return

    audio = wave.open(audio_in, 'rb')
    params = audio.getparams()
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    binary_message = text_to_binary(message) + '11111110'  # Stop bit

    if len(binary_message) > len(frames):
        print("Hata: Ses dosyası mesajı gizlemek için yeterli uzunlukta değil.")
        return

    for i in range(len(binary_message)):
        frames[i] = (frames[i] & 254) | int(binary_message[i])  # LSB'yi değiştir

    audio_out_file = wave.open(audio_out, 'wb')
    audio_out_file.setparams(params)
    audio_out_file.writeframes(frames)
    audio_out_file.close()
    print("[+] Mesaj başarıyla gömüldü.")

# Ses dosusundan mesajı çıkar
def extract_message(audio_path):
    audio = wave.open(audio_path, 'rb')
    frames = bytearray(list(audio.readframes(audio.getnframes())))
    audio.close()

    bits = []
    for i in range(len(frames)):
        bits.append(str(frames[i] & 1))
        if len(bits) >= 8 and ''.join(bits[-8:]) == '11111110':
            break

    binary_str = ''.join(bits[:-8])  # Stop bitten öncesini al
    return binary_to_text(binary_str)

# Ana menü
if __name__ == '__main__':
    print("1. Mesaj gizle")
    print("2. Mesaj çıkar")
    choice = input("Seçiminiz (1/2): ")

    if choice == '1':
        in_path = input("Girdi ses dosyası (örnek: input.wav): ")
        out_path = input("Çıktı dosyası adı (örnek: output.wav): ")
        msg = input("Gizlenecek mesaj (max 160 karakter): ")
        embed_message(in_path, out_path, msg)
    elif choice == '2':
        in_path = input("Mesaj gizlenmiş ses dosyası (örnek: output.wav): ")
        hidden_msg = extract_message(in_path)
        print("[+] Çıkarılan mesaj:", hidden_msg)
    else:
        print("Geçersiz seçim.")
