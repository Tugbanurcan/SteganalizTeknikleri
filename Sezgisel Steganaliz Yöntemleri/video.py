import wave
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip

# 1. Adım: Video'dan ses çıkarma
def extract_audio_from_video(video_path, audio_output_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_output_path)
        print(f"Audio extracted to: {audio_output_path}")
    except Exception as e:
        print(f"Error extracting audio: {e}")

# 2. Adım: Mesajı sese gömme (LSB Yöntemi)
def hide_message_in_audio(audio_path, message, output_audio_path):
    try:
        message_bin = ''.join(format(ord(c), '08b') for c in message)
        
        with wave.open(audio_path, 'rb') as audio:
            params = audio.getparams()
            frames = audio.readframes(params.nframes)
            audio_samples = np.frombuffer(frames, dtype=np.int16)

        for i in range(len(message_bin)):
            audio_samples[i] = (audio_samples[i] & 0xFFFE) | int(message_bin[i])  # LSB'yi mesaj bitine set et
        
        with wave.open(output_audio_path, 'wb') as new_audio:
            new_audio.setparams(params)
            new_audio.writeframes(audio_samples.tobytes())
        
        print(f"Message hidden in audio: {output_audio_path}")
    except Exception as e:
        print(f"Error hiding message in audio: {e}")

# 3. Adım: Gizli mesajı sesten çıkarma
def extract_message_from_audio(audio_path, message_length):
    try:
        with wave.open(audio_path, 'rb') as audio:
            params = audio.getparams()
            frames = audio.readframes(params.nframes)
            audio_samples = np.frombuffer(frames, dtype=np.int16)

        message_bin = ""
        for i in range(message_length * 8):
            message_bin += str(audio_samples[i] & 1)

        message = ""
        for i in range(0, len(message_bin), 8):
            byte = message_bin[i:i+8]
            message += chr(int(byte, 2))
        
        return message
    except Exception as e:
        print(f"Error extracting message from audio: {e}")
        return ""

# 4. Adım: Gizli mesajı içeren sesle video oluşturma
def add_audio_to_video(video_path, audio_path, output_video_path):
    try:
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        audio = audio.subclip(0, video.duration)
        
        video = video.set_audio(audio)
        video.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
        print(f"Video with hidden message saved to: {output_video_path}")
    except Exception as e:
        print(f"Error adding audio to video: {e}")

# Uygulama: Kullanıcıdan veri alarak işlem yapma
def steganography_app():
    print("Video Steganography Uygulamasına Hoşgeldiniz!")
    
    video_input_path = input("Lütfen video dosyasının yolunu girin: ")
    audio_output_path = "extracted_audio.wav"
    
    # Video'dan ses çıkarma
    extract_audio_from_video(video_input_path, audio_output_path)

    # Kullanıcıdan gizlenecek mesajı alma
    secret_message = input("160 karakterlik bir mesaj girin: ")
    
    if len(secret_message) > 160:
        print("Mesaj çok uzun! Lütfen sadece 160 karakter girin.")
        return

    audio_with_message_path = "audio_with_message.wav"
    
    # Mesajı sese gömme
    hide_message_in_audio(audio_output_path, secret_message, audio_with_message_path)
    
    # Sesle video oluşturma
    output_video_path = "video_with_message.mp4"
    add_audio_to_video(video_input_path, audio_with_message_path, output_video_path)

    # Mesajı çıkarma (test amacıyla)
    extracted_message = extract_message_from_audio(audio_with_message_path, len(secret_message))
    print(f"Çıkarılan Mesaj: {extracted_message}")

if __name__ == "__main__":
    steganography_app()
