import ollama
import os
import pymupdf

response = ollama.chat(
    model="granite3.2",
    messages=[
        {"role": "user", "content": "selma, nasılsın?"}],
)
print(response["message"]["content"])   


def search_text_files(keyword: str) -> str:
    directory = os.listdir("./files/")

    for fname in directory:
        file_path = os.path.join("./files/", fname)

        if os.path.isfile(file_path) and not fname.startswith('.'):
            
            # PDF dosyası
            if fname.endswith(".pdf"):
                document_text = ""
                doc = pymupdf.open(file_path)
                for page in doc:
                    document_text += page.get_text()
                doc.close()

                prompt = f"Respond only 'yes' or 'no', do not add any additional information. Is the following text about {keyword}? {document_text}"

                res = ollama.chat(
                    model="granite3.2",
                    messages=[{"role": "user", "content": prompt}]
                )

                if res['message']['content'].strip().lower() == "yes":
                    return file_path

            # TXT dosyası
            elif fname.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    file_content = f.read()

                prompt = f"Respond only 'yes' or 'no', do not add any additional information. Is the following text about {keyword}? {file_content}"

                res = ollama.chat(
                    model="granite3.2",
                    messages=[{"role": "user", "content": prompt}]
                )

                if res['message']['content'].strip().lower() == "yes":
                    return file_path

    # Hiç eşleşme bulunmazsa
    return "None"
