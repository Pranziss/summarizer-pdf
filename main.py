from miaow.extractor import extract_text
from chunks.chunker import chunk_text
from llm.brain import query_llm, is_chunk_valid  # include validator

text = extract_text("sample.pdf")
chunks = chunk_text(text)

valid_chunks = [c for c in chunks if is_chunk_valid(c)]

summary_parts = []

for i, chunk in enumerate(valid_chunks[:3]):  # First 3 valid chunks
    result = query_llm(chunk, task="summarize", model="phi")
    summary_parts.append(result)

# Clean, friendly summary output
final_summary = "\n".join(summary_parts)
print(f"\n📚 Summary of your study material:\n{final_summary}")