from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

app = FastAPI()

RUNPOD_API_URL = "https://jsgbk4z01cvmgz-80.proxy.runpod.net/generate"  # <-- Заменяй на свой!

@app.get("/generate/line")
def generate_line(
    prompt_type: str = Query(..., pattern="^(hook|quote|question)$"),
    prompt: str = Query(..., min_length=1)
):
    if prompt_type == "hook":
        full_prompt = f"Generate a catchy hook: {prompt}"
    elif prompt_type == "quote":
        full_prompt = f"Generate a short inspirational quote about: {prompt}"
    elif prompt_type == "question":
        full_prompt = f"Generate an engaging question about: {prompt}"
    else:
        return {"error": "Invalid prompt_type"}

    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 50,
            "temperature": 0.7,
            "top_p": 0.9,
            "repetition_penalty": 1.2,
            "stop": ["\n", "."]
        }
    }

    try:
        response = requests.post(RUNPOD_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        generated_text = result.get("generated_text", "").strip()

        if len(generated_text) < 5 or not any(c.isalpha() for c in generated_text):
            return {"response": "Generated text looks like gibberish, try again or change prompt."}
        return {"response": generated_text}

    except Exception as e:
        return {"error": str(e)}
