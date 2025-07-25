import requests

BASE_URL = "http://localhost:11434/api/generate"  # Ollama default API

def build_prompt(text: str, task: str) -> str:
    prompt_map = {
        "summarize": f"Summarize the following educational material. Focus on key points, structure, and learning objectives:\n{text}",
        "tone": f"Analyze the emotional tone and intent of this writing. Support your answer with reasoning:\n{text}",
        "flag": f"Review this content and highlight contradictions, vague areas, or overly complex phrasing:\n{text}",
        "rewrite": f"Rewrite the following text to improve clarity, readability, and logical flow. Preserve original meaning:\n{text}"
    }
    return prompt_map.get(task.lower(), f"Summarize:\n{text}")

def query_llm(text: str, task: str = "summarize", model: str = "phi") -> str:
    # Skip trivial chunks before making the request
    if not is_chunk_valid(text):
        return "⏭️ Skipped: Chunk too short or empty."

    prompt = build_prompt(text, task)
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(BASE_URL, json=payload)
    
    if response.ok:
        reply = response.json()["response"]
        # Gracefully handle vague replies
        if "don't have access" in reply.lower() or "can't answer" in reply.lower():
            return "⚠️ Vague answer—consider adjusting prompt or chunk context."
        return reply
    else:
        raise RuntimeError(f"LLM query failed: {response.status_code} - {response.text}")

def is_chunk_valid(chunk: str, min_length: int = 300) -> bool:
    """Filter out trivial or empty chunks"""
    return len(chunk.strip()) >= min_length and any(char.isalpha() for char in chunk)