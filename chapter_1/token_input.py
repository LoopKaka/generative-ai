import tiktoken as tk

encoding_model = tk.encoding_for_model("gpt-4o")
text = "I am LoopKaka"

encoded = encoding_model.encode(text)
print(encoded)