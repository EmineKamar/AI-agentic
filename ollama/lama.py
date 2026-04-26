import ollama
import os
import pymupdf
import fitz

def search_text_files(keyword: str) -> str:

  

  directory = os.listdir("./files/")

  for fname in directory:

    

    # look through all the files in our directory that aren't hidden files

    if os.path.isfile("./files/" + fname) and not fname.startswith('.'):



        if(fname.endswith(".pdf")):

           

           document_text = ""

           doc = pymupdf.open("./files/" + fname)



           for page in doc: # iterate the document pages

               document_text += page.get_text() # get plain text (is in UTF-8)

               

           doc.close()



           prompt = "Respond only 'yes' or 'no', do not add any additional information. Is the following text about " + keyword + "? " + document_text 



           res = ollama.chat(

                model="granite3.2",

                messages=[{'role': 'user', 'content': prompt}]

            )



           if 'Yes' in res['message']['content']:

                return "./files/" + fname



        elif(fname.endswith(".txt")):



            f = open("./files/" + fname, 'r')

            file_content = f.read()

            

            prompt = "Respond only 'yes' or 'no', do not add any additional information. Is the following text about " + keyword + "? " + file_content 



            res = ollama.chat(

                model="granite3.2",

                messages=[{'role': 'user', 'content': prompt}]

            )

           

            if 'Yes' in res['message']['content']:

                f.close()

                return "./files/" + fname



  return "None"


def search_text_files(keyword: str) -> str:

  

  directory = os.listdir("./files/")

  for fname in directory:

    

    # look through all the files in our directory that aren't hidden files

    if os.path.isfile("./files/" + fname) and not fname.startswith('.'):



        if(fname.endswith(".pdf")):

           

           document_text = ""

           doc = pymupdf.open("./files/" + fname)



           for page in doc: # iterate the document pages

               document_text += page.get_text() # get plain text (is in UTF-8)

               

           doc.close()



           prompt = "Respond only 'yes' or 'no', do not add any additional information. Is the following text about " + keyword + "? " + document_text 



           res = ollama.chat(

                model="granite3.2",

                messages=[{'role': 'user', 'content': prompt}]

            )



           if 'Yes' in res['message']['content']:

                return "./files/" + fname



        elif(fname.endswith(".txt")):



            f = open("./files/" + fname, 'r')

            file_content = f.read()

            

            prompt = "Respond only 'yes' or 'no', do not add any additional information. Is the following text about " + keyword + "? " + file_content 



            res = ollama.chat(

                model="granite3.2",

                messages=[{'role': 'user', 'content': prompt}]

            )

           

            if 'Yes' in res['message']['content']:

                f.close()

                return "./files/" + fname



  return "None"

def search_image_files(keyword:str) -> str:



    directory = os.listdir("./files/")

    image_file_types = ("jpg", "png", "jpeg")



    for fname in directory:



        if os.path.isfile("./files/" + fname) and not fname.startswith('.') and fname.endswith(image_file_types):

            res = ollama.chat(

                model="granite3.2-vision",

                messages=[

                    {

                        'role': 'user',

 
                       'content': 'Describe this image in short sentences. Use simple phrases first and then describe it more fully.',

                        'images': ["./files/" + fname]

                    }

                ]

            )



            if keyword in res['message']['content']:

                return "./files/" + fname

    

    return "None"


available_functions = {

  'Search inside text files':search_text_files,

  'Search inside image files':search_image_files

}
# tools don't need to be defined as an object but this helps pass the correct parameters

# to the tool call itself by giving the model a prompt of how the tool is to be used

ollama_tools=[

     {

      'type': 'function',

      'function': {

        'name': 'Search inside text files',

        'description': 'This tool searches in PDF or plaintext or text files in the local file system for descriptions or mentions of the keyword.',

        'parameters': {

          'type': 'object',

          'properties': {

            'keyword': {

              'type': 'string',

              'description': 'Generate one keyword from the user request to search for in text files',

            },

          },

          'required': ['keyword'],

        },

      },

    },

    {

      'type': 'function',

      'function': {

        'name': 'Search inside image files',

        'description': 'This tool searches for photos or image files in the local file system for the keyword.',

        'parameters': {

          'type': 'object',

          'properties': {

            'keyword': {

              'type': 'string',

              'description': 'Generate one keyword from the user request to search for in image files',

            },

          },

          'required': ['keyword'],

        },

      },

    },

  ]

# if ollama is not currently running, start it

import subprocess

# Ollama'yı arka planda başlat
process = subprocess.Popen(["ollama", "serve"])

print(process)
import subprocess
import time
import socket
import ollama

def is_port_in_use(host="127.0.0.1", port=11434):
    """Belirtilen portun kullanımda olup olmadığını kontrol eder."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

# Ollama çalışıyor mu kontrol et
if not is_port_in_use():
    print("Ollama başlatılıyor...")
    process = subprocess.Popen(["ollama", "serve"])
    time.sleep(5)  # Servisin başlaması için bekle
    print(process)
else:
    print("Ollama zaten çalışıyor, direkt bağlanılıyor...")

# Artık Python üzerinden modelle iletişim kurabilirsin
response = ollama.chat(
    model="granite3.2",
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)

print("Model cevabı:", response["message"]["content"])
