# Chat With Your Documents: Build a Local RAG App with Ollama

Companion repository for the **Code with Antonio** video course · [Watch on YouTube](https://youtu.be/hImbnQJLuRI).

Chat with your documents: a 100% local RAG app in Python that answers from your PDFs, citing file and page. Ollama, no cloud, no GPU.

## What you'll build

docchat: the PDFs of Lumen Bikes, a made-up company the model knows nothing about, are chunked, embedded with embeddinggemma and searched by cosine similarity; qwen3.5:4b answers citing file and page, first in the terminal and then in a Streamlit web chat where you upload a new PDF.

## Lessons

| # | Lesson | Video | Folder |
|---|---|---|---|
| 1 | What is RAG? | [0:00](https://youtu.be/hImbnQJLuRI?t=0) | [lessons/01-what-is-rag](lessons/01-what-is-rag) |
| 2 | Two models and a project | [3:00](https://youtu.be/hImbnQJLuRI?t=180) | [lessons/02-two-models-and-a-project](lessons/02-two-models-and-a-project) |
| 3 | Read and chunk your PDFs | [5:42](https://youtu.be/hImbnQJLuRI?t=342) | [lessons/03-read-and-chunk-your-pdfs](lessons/03-read-and-chunk-your-pdfs) |
| 4 | Turn text into vectors | [7:47](https://youtu.be/hImbnQJLuRI?t=467) | [lessons/04-turn-text-into-vectors](lessons/04-turn-text-into-vectors) |
| 5 | Search and answer with sources | [10:51](https://youtu.be/hImbnQJLuRI?t=651) | [lessons/05-search-and-answer-with-sources](lessons/05-search-and-answer-with-sources) |
| 6 | A chat UI with Streamlit | [13:49](https://youtu.be/hImbnQJLuRI?t=829) | [lessons/06-a-chat-ui-with-streamlit](lessons/06-a-chat-ui-with-streamlit) |
| 7 | Speed, limits and next steps | [16:43](https://youtu.be/hImbnQJLuRI?t=1003) | [lessons/07-speed-limits-and-next-steps](lessons/07-speed-limits-and-next-steps) |

## Requirements

- Ollama 0.35.0 · embeddinggemma (300M, 621 MB) · qwen3.5:4b (3.4 GB) · ollama-python 0.6.3 · pypdf 6.19.0 · numpy 2.5.3 · Streamlit 1.65.0 · uv 0.12.14 · Python 3.12 · Ubuntu (Linux), i7-1255U, 16 GB, no GPU
- Python 3.12+ and [uv](https://docs.astral.sh/uv/)

## Run the final project

```bash
cd app
ollama pull embeddinggemma
ollama pull qwen3.5:4b
uv sync
uv run ingest.py        # reads docs/*.pdf (sample PDFs of Lumen Bikes, a made-up company) and builds index/
uv run chat.py          # chat in the terminal
uv run streamlit run app.py   # the web chat on http://localhost:8501
```

## Repository structure

```
README.md          this file
lessons/           one folder per lesson: goal, timestamp, commands and files exactly as in the video
app/               the final working project
assets/            thumbnail
```

## License

MIT — use it for anything, credit appreciated.

---
Generated on 2026-10-04 from the course scripts. Code with Antonio · AI tutor.