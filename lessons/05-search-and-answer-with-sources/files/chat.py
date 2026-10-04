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
