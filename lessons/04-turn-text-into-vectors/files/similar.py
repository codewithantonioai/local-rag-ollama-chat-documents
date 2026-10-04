import numpy as np
import ollama

question = "Why does my bike's motor feel so hot?"
texts = [
    "E07: motor overheating. Let the motor cool down.",
    "Every employee gets 27 days of paid vacation.",
]

response = ollama.embed(model="embeddinggemma", input=[question, *texts])
vectors = np.array(response.embeddings)
print("numbers per text:", vectors.shape[1])

for text, vector in zip(texts, vectors[1:]):
    score = vectors[0] @ vector
    print(f"{score:.2f}  {text}")
