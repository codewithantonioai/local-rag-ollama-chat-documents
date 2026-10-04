# Lesson 5 · Search and answer with sources

▶ [Watch this lesson](https://youtu.be/hImbnQJLuRI?t=651) (starts at 10:51)

## Goal

Lesson five. Search and answer with sources.

## Commands and files (as shown in the video)

### `rag.py` · vscode search

```python
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
```

### `rag.py` · vscode prompt answer

```python
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
```

### `chat.py` · vscode chat

```python
from rag import answer, load_index

index = load_index()

while True:
    question = input("\nYou: ")
    if question in ("", "exit"):
        break
    hits, stream = answer(question, index)
    for chunk, score in hits:
        print(f"  {score:.2f}  {chunk['source']} p.{chunk['page']}")
    print("AI: ", end="")
    for token in stream:
        print(token, end="", flush=True)
    print()
```

### Terminal · term vacation

```bash
uv run chat.py
```

## Recap

So: the search is one multiplication and a sort. The prompt sets three rules: use the context, admit what you don't know, and cite. And the same small model went from making things up to answering correctly. Let's give it a proper interface.
