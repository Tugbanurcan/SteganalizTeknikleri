import cv2
import numpy as np
from tkinter import filedialog, messagebox, Tk, Label, Button, Entry

# Video dosyasına mesaj gömme
def embed_message_in_video(video_path, message, output_path):
    # Mesajı bitlere dönüştür + %% sonlandırma işareti
    binary_message = ''.join(format(ord(c), '08b') for c in message) + ''.join(format(ord(c), '08b') for c in '%%')

    # Video dosyasını aç
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    data_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Kareyi RGB formatına çevir
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                for k in range(3):  # RGB kanalları
                    if data_index < len(binary_message):
                        # LSB'yi değiştirme
                        frame[i, j, k] = frame[i, j, k] & 0xFE | int(binary_message[data_index])
                        data_index += 1
                    else:
                        break

        # Yeni kareyi yaz
        out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    cap.release()
    out.release()
    print("Mesaj başarıyla videoya gömüldü!")

# Video dosyasından mesaj çözme
def extract_message_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    binary_message = ''

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Kareyi RGB formatına çevir
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                for k in range(3):  # RGB kanalları
                    binary_message += str(frame[i, j, k] & 1)

    cap.release()

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
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    return file_path

# Arayüzdeki işlemler
def embed_message():
    video_path = choose_file()
    if not video_path:
        return
    message = message_entry.get()
    if len(message) > 160:
        messagebox.showerror("Hata", "Mesaj çok uzun! Lütfen 160 karakterle sınırlı bir mesaj girin.")
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".avi", filetypes=[("AVI Files", "*.avi")])
    if not output_path:
        return
    embed_message_in_video(video_path, message, output_path)
    messagebox.showinfo("Başarılı", "Mesaj başarıyla videoya gömüldü!")

def extract_message():
    video_path = choose_file()
    if not video_path:
        return
    message = extract_message_from_video(video_path)
    if message:
        messagebox.showinfo("Gizli Mesaj", f"Gizli Mesaj: {message}")
    else:
        messagebox.showerror("Hata", "Mesaj çözülemedi.")

# Ana pencereyi oluştur
root = Tk()
root.title("Videoya Mesaj Gömme ve Çözme")

# Mesaj girişi
message_label = Label(root, text="Mesajı Girin (en fazla 160 karakter):")
message_label.pack(pady=10)
message_entry = Entry(root, width=50)
message_entry.pack(pady=10)

# Mesajı videoya gömme butonu
embed_button = Button(root, text="Mesajı Videoya Göm", command=embed_message)
embed_button.pack(pady=10)

# Mesajı videodan çözme butonu
extract_button = Button(root, text="Videodaki Mesajı Çöz", command=extract_message)
extract_button.pack(pady=10)

# Arayüzü başlat
root.mainloop()
