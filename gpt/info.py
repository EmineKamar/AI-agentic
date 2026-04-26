# 1. async/await
#python'da eşzamanlı işlemleri verimli yapmak için kullanılır.


#örn: aynı anda API' ye istek atmak

import asyncio
import httpx

async def fetch(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        return r.text
    
async def main():
    urls = ["https://example.com", "https://httpbin.org/get"]
    results = await asyncio.gather(*(fetch(u) for u in urls))
    print(results)

asyncio.run(main())

# 2. typing
# Kodunu daha okunabilir ve anlaşılır hale getirmek için kullanılır.
#örn: fonksiyonların parametre ve dönüş tiplerini belirtmek
from typing import List, Dict

def tokenize(text: str) -> List[str]:
    return text.split()

def word_count(tokens: List[str]) -> Dict[str, int]:
    return {t: tokens.count(t) for t in set(tokens)}

# IDE'ler ve tip denetleyiciler, bu ipuçlarını kullanarak hataları önceden tespit edebilir.



# 3. context managers
# Kaynak açma ve kapama işlemlerini otomatikleştirmek için kullanılır.with bloğu içinde kullanılır.
#örn: dosya işlemleri

with open ("data.txt", "r") as f:
    data = f.read() #dosya otomatik kapanır
    print(data)

# contextlib modülü ile kendi context manager'ını oluşturmak
from contextlib import contextmanager   
@contextmanager
def open_file(file, mode):
    f = open(file, mode)
    try:
        yield f # with bloğunun içine geçer
    finally:
        f.close() # dosya kapanır       
with open_file("data.txt", "r") as f:
    data = f.read()
    print(data)

# kendi context manager'ını oluşturmak

class Demo:
    def __enter(self):
        print("Açıldı")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Kapandı")

with Demo() as d:
    print("İçerideyim")


# 4. exceptions
# Hata yönetimi için kullanılır.

try:
    result = 24 / 0
except ZeroDivisionError:
    print("Sıfıra bölme hatası!")
finally:
    print("Bu blok her durumda çalışır.")

# Kendi özel exception sınıfını oluşturmak
class CustomError(Exception):
    pass    
def risky_function():
    raise CustomError("Özel bir hata oluştu!")
try:
    risky_function()
except CustomError as e:
    print(e)


################### API KULLANIMI #####################


# requests kütüphanesi ile API'ye istek atmak REST (HTTP)
import requests
response = requests.get("https://api.github.com")
print(response.status_code)  # Durum kodu
print(response.json())       # JSON yanıtı
print(response.headers)    # Başlık bilgileri

#Asenkron istekler için httpx kütüphanesi
import httpx, asyncio

async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com")
        print(r.json())

asyncio.run(main())

# API'ye veri göndermek (POST isteği)
data = {"key": "value"}
response = requests.post("https://httpbin.org/post", json=data)
print(response.json())
print(response.status_code)
print(response.headers)
print(response.text)  # Yanıt metni
print(response.content)  # Yanıt içeriği (bytes)
print(response.url)  # İstek yapılan URL
print(response.cookies)  # Çerezler
print(response.elapsed)  # İstek süresi
print(response.request.headers)  # İstek başlıkları
print(response.request.body)  # İstek gövdesi
print(response.history)  # Yönlendirme geçmişi
print(response.ok)  # Başarılı mı?
print(response.is_redirect)  # Yönlendirme mi?
print(response.links)  # Bağlantılar
print(response.raise_for_status())  # Hata varsa istisna fırlatır
print(response.iter_content(chunk_size=10))  # İçeriği parça parça okuma
print(response.iter_lines())  # Satır satır okuma
print(response.raw)  # Ham yanıt
print(response.apparent_encoding)  
print(response.encoding) 
print(response.close())  # Bağlantıyı kapatma
print(response.json())  # JSON yanıtı

# WebSocket ile gerçek zamanlı iletişim(streaming)
#gerçek zamanlı veri akışı için kullanılır.

import asyncio
import websockets

async def listen():
    async with websockets.connect("wss://echo.websocket.events") as ws:
        await ws.send("Merhaba WebSocket!")
        response = await ws.recv()
        print(f"Gelen mesaj: {response}")

asyncio.run(listen())

##### Tool Signatures #####
# Fonksiyonların parametre ve dönüş tiplerini belirtmek için kullanılır.
from typing import List, Dict
def process_data(data: List[int]) -> Dict[str, int]:
    return {"sum": sum(data), "count": len(data)}   
result = process_data([1, 2, 3, 4])
print(result)
print(process_data.__annotations__)  # {'data': typing.List[int], 'return': typing.Dict[str, int]}
# Bu, kodun okunabilirliğini artırır ve IDE'lerin daha iyi destek sağlamasına yardımcı olur.
# Özellikle büyük projelerde ve ekip çalışmalarında faydalıdır.
# Özetle, async/await, typing, context managers ve exceptions Python'da modern ve etkili kod yazmak için önemli araçlardır. API kullanımı ise uygulamalar arasında veri alışverişi için kritik bir yetenektir.
# Bu araçları ve teknikleri kullanarak daha verimli, okunabilir ve hatasız kodlar yazabilirsiniz.


############ MODEL API'LERİ #############

# OpenAI API kullanımı

from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4.1-turbo",
    messages=[
        {"role": "user", "content": "Merhaba, nasılsın?"}
    ]   
)
print(resp.choices[0].message.content)

# Anthropic (Claude) API kullanımı
from anthropic import Anthropic, Message
client = Anthropic()

resp = client.messages.create(
    model="claude-3-5-sonnet-2024-09-18",
    messages=[{"role": "user", "content": "Merhaba, nasılsın?"}],
    max_tokens=1024,
    temperature=0.7,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=["\n\nHuman:"]

)
print(resp.content[0].text)



# HuggingFace Inference 
from huggingface_hub import InferenceClient
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2")
resp = client.text_generation("Quantum computing nedir?")
print(resp)







