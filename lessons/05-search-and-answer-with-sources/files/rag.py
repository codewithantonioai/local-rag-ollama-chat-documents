import json
from pathlib import Path

import numpy as np
import ollama

EMBED_MODEL = "embeddinggemma"
CHAT_MODEL = "qwen3.5:4b"
TOP_K = 4

PROMPT = """Answer the question using only the context below.
If the answer is not in the context, say "I don't know".
Answer in two or three sentences, and cite the source of each fact
like [warranty-policy.pdf p.1].

Context:
{context}

Question: {question}"""


def load_index():
    chunks = json.loads(Path("index/chunks.json").read_text())
    return chunks, np.load("index/vectors.npy")


def search(question, index, k=TOP_K):
    chunks, vectors = index
    query = f"task: search result | query: {question}"
    response = ollama.embed(model=EMBED_MODEL, input=query)
    scores = vectors @ np.array(response.embeddings[0])
    best = np.argsort(scores)[::-1][:k]
    return [(chunks[i], float(scores[i])) for i in best]


def answer(question, index):
    hits = search(question, index)
    context = "\n\n".join(
        f"[{c['source']} p.{c['page']}]\n{c['text']}" for c, _ in hits)
    prompt = PROMPT.format(context=context, question=question)
    stream = ollama.chat(model=CHAT_MODEL, think=False, stream=True,
                         messages=[{"role": "user", "content": prompt}])
    return hits, (part.message.content for part in stream)
