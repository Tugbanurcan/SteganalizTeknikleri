from tkinter import filedialog, messagebox, Tk, Label, Button, Entry
from PIL import Image
import numpy as np

# Mesajı resme gömme
def embed_message_in_image(image_path, message, output_path):
    # Mesajı bitlere dönüştür + %% sonlandırma işareti
    binary_message = ''.join(format(ord(c), '08b') for c in message) + ''.join(format(ord(c), '08b') for c in '%%')

    # Resmi aç
    image = Image.open(image_path)
    pixels = np.array(image)

    data_index = 0
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):  # RGB
                if data_index < len(binary_message):
                    # En düşük anlamlı biti (LSB) değiştir
                    pixels[i, j][k] = pixels[i, j][k] & 0xFE | int(binary_message[data_index])
                    data_index += 1
                else:
                    break

    # Yeni resmi kaydet
    new_image = Image.fromarray(pixels)
    new_image.save(output_path)
    print("Mesaj başarıyla resme gömüldü!")

# Resimden mesajı çözme
def extract_message_from_image(image_path):
    image = Image.open(image_path)
    pixels = np.array(image)

    binary_message = ''
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            for k in range(3):  # RGB
                binary_message += str(pixels[i, j][k] & 1)

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
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp;*.jpg")])
    return file_path

# Arayüzdeki işlemler
def embed_message():
    image_path = choose_file()
    if not image_path:
        return
    message = message_entry.get()
    if len(message) > 160:
        messagebox.showerror("Hata", "Mesaj çok uzun! Lütfen 160 karakterle sınırlı bir mesaj girin.")
        return
    output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
    if not output_path:
        return
    embed_message_in_image(image_path, message, output_path)
    messagebox.showinfo("Başarılı", "Mesaj başarıyla resme gömüldü!")

def extract_message():
    image_path = choose_file()
    if not image_path:
        return
    message = extract_message_from_image(image_path)
    if message:
        messagebox.showinfo("Gizli Mesaj", f"Gizli Mesaj: {message}")
    else:
        messagebox.showerror("Hata", "Mesaj çözülemedi.")

# Ana pencereyi oluştur
root = Tk()
root.title("Resme Mesaj Gömme ve Çözme")

# Mesaj girişi
message_label = Label(root, text="Mesajı Girin (en fazla 160 karakter):")
message_label.pack(pady=10)
message_entry = Entry(root, width=50)
message_entry.pack(pady=10)

# Mesajı resme gömme butonu
embed_button = Button(root, text="Mesajı Resme Göm", command=embed_message)
embed_button.pack(pady=10)

# Mesajı resimden çözme butonu
extract_button = Button(root, text="Resimdeki Mesajı Çöz", command=extract_message)
extract_button.pack(pady=10)

# Arayüzü başlat
root.mainloop()
