import cv2
import numpy as np

# Mesajı resme gömmek için fonksiyon
def embed_message(image_path, message, output_path):
    # Resmi oku
    image = cv2.imread(image_path)
    
    # Mesajı sonlandırmak için bir işaret (terminator)
    message += '%%'
    
    # Mesajı bitlere dönüştür
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    
    # Mesaj uzunluğuna göre piksel sayısını kontrol et
    if len(binary_message) > image.size:
        raise ValueError("Mesaj çok büyük, resme sığmaz!")
    
    data_index = 0
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            for channel in range(image.shape[2]):
                # Eğer mesaj bitti ise, çık
                if data_index >= len(binary_message):
                    break
                # Pikselin RGB değerinin en düşük bitini değiştir
                pixel_value = image[row, col, channel]
                # En düşük anlamlı biti değiştir (LSB)
                new_pixel_value = (pixel_value & 0b11111110) | int(binary_message[data_index])
                image[row, col, channel] = new_pixel_value
                data_index += 1

    # Yeni resmi kaydet
    cv2.imwrite(output_path, image)
    print("Mesaj başarıyla gömüldü!")

# Örnek kullanım
# embed_message('tatil.jpg', 'Bu bir test mesajıdır.', 'output_image.png')



import cv2  # OpenCV kütüphanesini import ediyoruz
import numpy as np

def extract_message(image_path):
    # Resmi oku
    image = cv2.imread(image_path)
    
    binary_message = ''
    for row in range(image.shape[0]):
        for col in range(image.shape[1]):
            for channel in range(image.shape[2]):
                # Pikselin RGB değerinin en düşük bitini al
                pixel_value = image[row, col, channel]
                binary_message += str(pixel_value & 1)

    # Binari mesajı çöz
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))
        if message.endswith('%%'):  # Mesajın sonlandırma işareti
            break
    
    return message[:-2]  # '%%' işaretini kes

# Örnek kullanım
#message = extract_message('output_image.png')
#print("Gizli mesaj:", message)



# Kullanıcıdan giriş al
def main():
    print("Gizli mesaj uygulamasına hoş geldiniz!")
    
    while True:
        print("\nSeçim yapın:")
        print("1. Mesajı resme gömme")
        print("2. Resimden gizli mesajı çözme")
        print("3. Çıkış")
        
        choice = input("Seçiminizi yapın (1/2/3): ")
        
        if choice == '1':
            image_path = 'tatil.jpg'
            message = input("Gizlemek istediğiniz mesajı girin (en fazla 160 karakter): ")
            if len(message) > 160:
                print("Mesaj çok uzun! Lütfen 160 karakterle sınırlı bir mesaj girin.")
                continue
            embed_message(image_path, message,'output_image.png')
        
        elif choice == '2':
            image_path = input("Gizli mesajı çözmek istediğiniz resmi  girin: ")
            hidden_message = extract_message(image_path)
            if hidden_message:
                 
                print("Gizli mesaj:", hidden_message)
            else:
                print("Mesaj çözülemedi.")
        
        elif choice == '3':
            print("Uygulamadan çıkılıyor...")
            break
        else:
            print("Geçersiz seçim! Lütfen geçerli bir seçenek girin.")

# Uygulamayı başlat
if __name__ == "__main__":
    main()
