# Lesson 6 · A chat UI with Streamlit

▶ [Watch this lesson](https://youtu.be/hImbnQJLuRI?t=829) (starts at 13:49)

## Goal

Lesson six. A chat UI with Streamlit.

## Commands and files (as shown in the video)

### Terminal · term add streamlit

```bash
uv add streamlit
```

### `.streamlit/config.toml` · vscode config

```yaml
[server]
address = "localhost"
headless = true

[browser]
gatherUsageStats = false

[client]
toolbarMode = "minimal"

[theme]
base = "dark"
primaryColor = "#4FEBFF"
```

### `app.py` · vscode app chat

```python
from pathlib import Path

import streamlit as st

from ingest import build
from rag import answer, load_index

st.title("Chat with your documents")


@st.cache_resource
def get_index():
    return load_index()


with st.sidebar:
    st.header("Documents")
    for pdf in sorted(Path("docs").glob("*.pdf")):
        st.write(pdf.name)
    upload = st.file_uploader("Add a PDF", type="pdf")
    if upload and st.button("Add and re-index"):
        Path("docs", upload.name).write_bytes(upload.getvalue())
        with st.spinner("Reading and embedding..."):
            build()
        get_index.clear()
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask about your PDFs"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        hits, stream = answer(question, get_index())
        reply = st.write_stream(stream)
        with st.expander("Sources"):
            for chunk, score in hits:
                name = f"**{chunk['source']}** p.{chunk['page']}"
                st.markdown(f"{name} · {score:.2f}")
                st.caption(chunk["text"])
    st.session_state.messages.append({"role": "assistant", "content": reply})
```

### `app.py` · vscode app sidebar

```python
from pathlib import Path

import streamlit as st

from ingest import build
from rag import answer, load_index

st.title("Chat with your documents")


@st.cache_resource
def get_index():
    return load_index()


with st.sidebar:
    st.header("Documents")
    for pdf in sorted(Path("docs").glob("*.pdf")):
        st.write(pdf.name)
    upload = st.file_uploader("Add a PDF", type="pdf")
    if upload and st.button("Add and re-index"):
        Path("docs", upload.name).write_bytes(upload.getvalue())
        with st.spinner("Reading and embedding..."):
            build()
        get_index.clear()
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask about your PDFs"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        hits, stream = answer(question, get_index())
        reply = st.write_stream(stream)
        with st.expander("Sources"):
            for chunk, score in hits:
                name = f"**{chunk['source']}** p.{chunk['page']}"
                st.markdown(f"{name} · {score:.2f}")
                st.caption(chunk["text"])
    st.session_state.messages.append({"role": "assistant", "content": reply})
```

### Terminal · term streamlit run

```bash
uv run streamlit run app.py
```

## Recap

So: Streamlit reruns your script on every interaction, session state and cache resource keep what matters, and you can add a PDF and ask about it straight away. Now, how good is it really?
