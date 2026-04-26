import os
import time
import socket
import subprocess
import fitz
import ollama

# ---------------- Ollama Servis Kontrol ----------------
def is_port_in_use(host="127.0.0.1", port=11434):
    """Belirtilen portun kullanımda olup olmadığını kontrol eder."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

if not is_port_in_use():
    print("Ollama başlatılıyor...")
    process = subprocess.Popen(["ollama", "serve"])
    time.sleep(5)  # Servisin başlaması için bekle
    print(process)
else:
    print("Ollama zaten çalışıyor, direkt bağlanılıyor...")

# ---------------- Dosya Arama ----------------
def search_files(keyword: str) -> dict:
    """
    PDF, TXT ve resim dosyalarında arama yapar.
    Dönen değer: {"text": [dosya yolları], "images": [dosya yolları]}
    """
    directory = "./files/"
    image_types = (".jpg", ".jpeg", ".png")
    found_texts = []
    found_images = []

    for fname in os.listdir(directory):
        path = os.path.join(directory, fname)
        if not os.path.isfile(path) or fname.startswith('.'):
            continue

        # PDF ve TXT dosyaları
        if fname.endswith(".pdf"):
            doc_text = ""
            doc = fitz.open(path)
            for page in doc:
                doc_text += page.get_text()
            doc.close()
            prompt = f"Respond only 'yes' or 'no'. Is the following text about {keyword}? {doc_text}"
            res = ollama.chat(model="granite3.2", messages=[{"role": "user", "content": prompt}])
            if 'yes' in res['message']['content'].lower():
                found_texts.append(path)

        elif fname.endswith(".txt"):
            with open(path, 'r', encoding='utf-8') as f:
                file_text = f.read()
            prompt = f"Respond only 'yes' or 'no'. Is the following text about {keyword}? {file_text}"
            res = ollama.chat(model="granite3.2", messages=[{"role": "user", "content": prompt}])
            if 'yes' in res['message']['content'].lower():
                found_texts.append(path)

        # Resim dosyaları
        elif fname.lower().endswith(image_types):
            res = ollama.chat(model="granite3.2-vision", messages=[{
                "role": "user",
                "content": "Describe this image in short sentences. Use simple phrases first and then describe it more fully.",
                "images": [path]
            }])
            if keyword.lower() in res['message']['content'].lower():
                found_images.append(path)

    return {"text": found_texts, "images": found_images}

# ---------------- Kullanıcı Etkileşimi ----------------
keyword = input("Aramak istediğiniz kelimeyi girin: ")
results = search_files(keyword)

print("\n--- Arama Sonuçları ---")
if results["text"]:
    print("Text/PDF dosyaları bulundu:")
    for f in results["text"]:
        print("  -", f)
else:
    print("Text/PDF dosyası bulunamadı.")

if results["images"]:
    print("Image dosyaları bulundu:")
    for f in results["images"]:
        print("  -", f)
else:
    print("Image dosyası bulunamadı.")

# ---------------- Test Mesajı ----------------
response = ollama.chat(model="granite3.2", messages=[{"role": "user", "content": "Hello, how are you?"}])
print("\nModel cevabı:", response["message"]["content"])
