import tkinter as tk
from tkinter import filedialog, messagebox
import wave
import numpy as np

# Ses dosyasına mesaj gömme
def embed_message_in_audio(audio_path, message, output_path):
    # Mesajı bitlere dönüştür + %% sonlandırma işareti
    binary_message = ''.join(format(ord(c), '08b') for c in message) + ''.join(format(ord(c), '08b') for c in '%%')

    audio = wave.open(audio_path, 'rb')
    frames = audio.readframes(audio.getnframes())
    frames_array = np.frombuffer(frames, dtype=np.int16)

    # NumPy array'ini kopyalayarak değiştirilebilir yap
    frames_array = frames_array.copy()

    data_index = 0
    for i in range(len(frames_array)):
        if data_index < len(binary_message):
            frames_array[i] = (frames_array[i] & 0xFFFE) | int(binary_message[data_index])
            data_index += 1
        else:
            break

    new_audio = wave.open(output_path, 'wb')
    new_audio.setparams(audio.getparams())
    new_audio.writeframes(frames_array.tobytes())
    new_audio.close()
    print("Mesaj başarıyla ses dosyasına gömüldü!")

# Ses dosyasından mesaj çözme
def extract_message_from_audio(audio_path):
    audio = wave.open(audio_path, 'rb')
    frames = audio.readframes(audio.getnframes())
    frames_array = np.frombuffer(frames, dtype=np.int16)

    binary_message = ''
    for frame in frames_array:
        binary_message += str(frame & 1)  # En düşük anlamlı bit (LSB) al

    # Mesajı çöz
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    # '%%' işaretini kontrol et ve kes
    end_marker = '%%'
    if message.endswith(end_marker):
        message = message[:-len(end_marker)]  # Sadece '%%' işaretini kes
    return message

# Dosya seçme fonksiyonu
def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV Files", "*.wav")])
    return file_path

# Arayüzdeki işlemler
def embed_message():
    audio_path = choose_file()
    if not audio_path:
        return
    message = message_entry.get()
    if len(message) > 160:
        messagebox.showerror("Hata", "Mesaj çok uzun! Lütfen 160 karakterle sınırlı bir mesaj girin.")
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
    if not output_path:
        return
    embed_message_in_audio(audio_path, message, output_path)
    messagebox.showinfo("Başarılı", "Mesaj başarıyla ses dosyasına gömüldü!")

def extract_message():
    audio_path = choose_file()
    if not audio_path:
        return
    message = extract_message_from_audio(audio_path)
    if message:
        messagebox.showinfo("Gizli Mesaj", f"Gizli Mesaj: {message}")
    else:
        messagebox.showerror("Hata", "Mesaj çözülemedi.")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Ses Dosyasına Mesaj Gömme ve Çözme")

# Mesaj girişi
message_label = tk.Label(root, text="Mesajı Girin (en fazla 160 karakter):")
message_label.pack(pady=10)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=10)

# Mesajı ses dosyasına gömme butonu
embed_button = tk.Button(root, text="Mesajı Ses Dosyasına Göm", command=embed_message)
embed_button.pack(pady=10)

# Mesajı ses dosyasından çözme butonu
extract_button = tk.Button(root, text="Ses Dosyasındaki Mesajı Çöz", command=extract_message)
extract_button.pack(pady=10)

# Arayüzü başlat
root.mainloop()
