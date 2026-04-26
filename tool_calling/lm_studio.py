import lmstudio as lms
model = lms.llm("ibm-granite/granite-3.3-8b-instruct-GGUF")

print(model.respond("Hello Granite!"))

def add(a: float, b:float):
    """Given two numbers a and b, return a + b."""
    return a + b

def subtract(a: float, b:float):
    """Given two numbers a and b, return a - b."""
    return a - b

def multiply(a: float, b: float):
    """Given two numbers a and b, return a * b."""
    return a * b

def divide(a: float, b: float):
    """Given two numbers a and b, return a / b."""
    return a / b

def exp(a: float, b:float):
    """Given two numbers a and b, return a^b"""
    return a ** b


model.act(
  "What is 26.97 divided by 6.28? Don't round.",
  [add, subtract, multiply, divide, exp],
  on_message=print,
)

print(model.respond("How many Bs are in the word 'blackberry'?"))

def get_letter_frequency(word: str) -> dict:
    """Takes in a word (string) and returns a dictionary containing the counts of each letter that appears in the word. """

    letter_frequencies = {}

    for letter in word:
        if letter in letter_frequencies:
            letter_frequencies[letter] += 1
        else:
            letter_frequencies[letter] = 1

    return letter_frequencies

model.act(
  "How many Bs are in the word 'blackberry'?",
  [get_letter_frequency],
  on_message=print,
)