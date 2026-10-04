# Lesson 2 · Two models and a project

▶ [Watch this lesson](https://youtu.be/hImbnQJLuRI?t=180) (starts at 3:00)

## Goal

Lesson two. Two models and a project.

## Commands and files (as shown in the video)

### Terminal · term pull

```bash
ollama pull embeddinggemma
ollama pull qwen3.5:4b
```

### Terminal · term list

```bash
ollama list
```

### Terminal · term no rag

```bash
ollama run qwen3.5:4b --think=false "How many vacation days do new employees get at Lumen Bikes?"
```

### Terminal · term uv init

```bash
uv init --no-package docchat
cd docchat
uv add ollama pypdf numpy
```

### Terminal · term docs

```bash
ls docs
uv run main.py
```

## Recap

So far: embedding Gemma will find things, Qwen will answer, and we have a uv project with our PDFs. Time to read them.
