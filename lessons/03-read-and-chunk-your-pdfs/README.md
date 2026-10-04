# Lesson 3 · Read and chunk your PDFs

▶ [Watch this lesson](https://youtu.be/hImbnQJLuRI?t=342) (starts at 5:42)

## Goal

Lesson three. Read and chunk your PDFs.

## Commands and files (as shown in the video)

### `ingest.py` · vscode read pdfs

```python
from pathlib import Path

from pypdf import PdfReader

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


if __name__ == "__main__":
    pages = read_pdfs("docs")
    chunks = chunk(pages)
    print(f"{len(pages)} pages -> {len(chunks)} chunks")
    first = chunks[1]
    print(f"[{first['source']} p.{first['page']}]")
    print(first["text"])
```

### `ingest.py` · vscode chunk

```python
from pathlib import Path

from pypdf import PdfReader

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


if __name__ == "__main__":
    pages = read_pdfs("docs")
    chunks = chunk(pages)
    print(f"{len(pages)} pages -> {len(chunks)} chunks")
    first = chunks[1]
    print(f"[{first['source']} p.{first['page']}]")
    print(first["text"])
```

### Terminal · term ingest v1

```bash
uv run ingest.py
```

## Recap

So: pypdf extracts the text, we cut it into chunks of a hundred and twenty words with an overlap of thirty, and every chunk remembers its file and page. Next, we give each chunk its meaning in numbers.
