import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens for a given text."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Examples
examples = [
    "Hello, world!",
    "def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)",
    "The quick brown fox jumps over the lazy dog.",
    "supercalifragilisticexpialidocious",
]

for text in examples:
    tokens = count_tokens(text)
    ratio = len(text) / tokens
    print(f"{tokens:3d} tokens | {len(text):3d} chars | ratio: {ratio:.1f} | {text[:50]}...")