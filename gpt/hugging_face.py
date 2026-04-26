from transformers import pipeline 

generator = pipeline(
    "text-generation",
    model = "mistralai/Mistral-7B-Instruct-v0.2",
    device = 0
)

prompt = "Quantum computing nedir?"

result = generator(prompt, max_length=100, do_sample=True, temperature=0.7)

print("model output:", result[0]['generated_text'])
