# Lesson 4 · Turn text into vectors

▶ [Watch this lesson](https://youtu.be/hImbnQJLuRI?t=467) (starts at 7:47)

## Goal

Lesson four. Turn text into vectors.

## Commands and files (as shown in the video)

### Terminal · term hello world

```bash
ollama run embeddinggemma "Hello world"
```

### `similar.py` · vscode similar

```python
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
```

### Terminal · term similar

```bash
uv run similar.py
```

### `ingest.py` · vscode embed build

```python
import json
from pathlib import Path

import numpy as np
import ollama
from pypdf import PdfReader

EMBED_MODEL = "embeddinggemma"
CHUNK_WORDS = 120
OVERLAP = 30


def read_pdfs(folder):
    pages = []
    for pdf in sorted(Path(folder).glob("*.pdf")):
        for number, page in enumerate(PdfReader(pdf).pages, start=1):
            pages.append({"source": pdf.name, "page": number,
                          "text": page.extract_text()})
    return pages


def chunk(pages):
    chunks = []
    step = CHUNK_WORDS - OVERLAP
    for p in pages:
        words = p["text"].split()
        for start in range(0, len(words), step):
            text = " ".join(words[start:start + CHUNK_WORDS])
            chunks.append({"source": p["source"], "page": p["page"],
                           "text": text})
            if start + CHUNK_WORDS >= len(words):
                break
    return chunks


def embed(texts):
    docs = [f"title: none | text: {t}" for t in texts]
    response = ollama.embed(model=EMBED_MODEL, input=docs)
    return np.array(response.embeddings, dtype=np.float32)


def build(folder="docs"):
    chunks = chunk(read_pdfs(folder))
    vectors = embed([c["text"] for c in chunks])
    Path("index").mkdir(exist_ok=True)
    np.save("index/vectors.npy", vectors)
    Path("index/chunks.json").write_text(json.dumps(chunks, indent=2))
    print(f"indexed {len(chunks)} chunks -> {vectors.shape}")


if __name__ == "__main__":
    build()
```

### Terminal · term ingest

```bash
time uv run ingest.py
LC_ALL=C ls -lh index
```

## Recap

So: an embedding is meaning as numbers. With normalized vectors, cosine similarity is just a dot product. And our index is two files, vectors and chunks. Now let's ask it something.
