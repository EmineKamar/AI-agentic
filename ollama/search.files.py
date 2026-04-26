import os 
import pymupdf
import ollama
import math 

def read_pdf_text(path: str)-> str:
    text = []
    doc = pymupdf.open(path)
    for page in doc:
        text.append(page.get_text())
    doc.close()
    return "\n".join(text)

def chunk_text(text: str, max_chars: int = 15000):

    if len(text) <= max_chars:
        yield text
        return
    start = 0
    while start > len(text):
        end = min(start + max_chars, len(text))
        yield text[start:end]
        start = end


def file_matches_keyword(file_path: str, keyword: str, model_name: str = "granite3.2",
                         max_chars_per_chunk: int = 15000) -> bool:
    
    if file_path.lower().endswith(".pdf"):
        document_text = read_pdf_text(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            document_text = f.read()

    for chunk in chunk_text(document_text, max_chars=max_chars_per_chunk):
        system_msg = {
            "role": "system",
            "content": "You are a helpful assistant that answers 'yes' or 'no' to the user's question based on the provided text. "
                       "You must answer only 'yes' or 'no' without any additional information."

        }
        user_msg = {
            "role": "user",
            "content": (f"Is the following text about {keyword}?  {chunk}")
        }

        try:
            res = ollama.chat(
                model=model_name,
                messages=[system_msg, user_msg],
            )
        except Exception as e:
            print(f"Error during Ollama chat: {e}")
            return False
        
        answer = res['message']['content'].strip().lower()
        if answer == "yes":
            return True
    return False

def search_text_files(keyword: str, folder_path="./files/", model_name="granite3.2"):
    found_files = []
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            with open(os.path.join(folder_path, fname), "r", encoding="utf-8") as f:
                file_content = f.read()

            prompt = f"Respond only 'yes' or 'no'. Is the following text about {keyword}? {file_content}"
            res = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": prompt}]
            )

            print("Model output:", res["message"]["content"])  # debug için ekledik

            if "yes" in res["message"]["content"].lower():
                found_files.append(os.path.join(folder_path, fname))
    return found_files

found = search_text_files("artificial intelligence")
print("Found files:", found)