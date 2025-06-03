from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Text Generator — Modern UI</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet" />
<style>
    /* Gradient background animation */
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    body {
        margin: 0;
        min-height: 100vh;
        font-family: 'Inter', sans-serif;
        background: linear-gradient(270deg, #007CF0, #00DFD8, #7928CA, #FF0080);
        background-size: 800% 800%;
        animation: gradientBG 15s ease infinite;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        color: #fff;
        flex-direction: column;
    }

    h1 {
        font-weight: 700;
        font-size: 3rem;
        text-align: center;
        text-shadow: 0 2px 10px rgba(0,0,0,0.4);
        margin-bottom: 1rem;
        user-select: none;
    }

    form {
        background: rgba(255,255,255,0.1);
        padding: 1.8rem 2rem;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        backdrop-filter: blur(12px);
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
        max-width: 600px;
        width: 100%;
        user-select: none;
    }

    input[type="text"] {
        flex: 1 1 60%;
        padding: 0.8rem 1rem;
        font-size: 1.2rem;
        border: none;
        border-radius: 8px;
        outline: none;
        transition: box-shadow 0.3s ease;
    }

    input[type="text"]:focus {
        box-shadow: 0 0 8px 2px #00FFD1;
        background: rgba(255,255,255,0.15);
        color: #fff;
    }

    button {
        flex: 1 1 30%;
        background: linear-gradient(135deg, #00FFD1, #007CF0);
        border: none;
        color: #222;
        font-weight: 700;
        font-size: 1.2rem;
        border-radius: 8px;
        cursor: pointer;
        transition: background 0.3s ease, transform 0.2s ease;
        user-select: none;
        box-shadow: 0 4px 15px rgba(0,255,209,0.5);
    }

    button:hover {
        background: linear-gradient(135deg, #007CF0, #00FFD1);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(0,255,209,0.75);
    }

    .result {
        margin-top: 2rem;
        background: rgba(0,0,0,0.5);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        max-width: 600px;
        width: 100%;
        animation: fadeIn 1s ease forwards;
        user-select: text;
    }

    .result p {
        margin: 0.5rem 0;
        font-size: 1.15rem;
        line-height: 1.4;
    }

    .label-bold {
        font-weight: 700;
        color: #00FFD1;
    }

    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }

    @media (max-width: 480px) {
        h1 { font-size: 2.2rem; }
        input[type="text"], button {
            flex: 1 1 100%;
        }
    }
</style>
</head>
<body>
    <h1>Topic Text Generator</h1>
    <form method="post" autocomplete="off" spellcheck="false">
        <input type="text" name="prompt" id="prompt" placeholder="Enter topic..." value="{{prompt}}" required autofocus />
        <button type="submit" aria-label="Generate text">Generate</button>
    </form>

    {% if response_text %}
    <div class="result" role="region" aria-live="polite">
        <p><span class="label-bold">Server response:</span> {{response_text}}</p>
        <p><span class="label-bold">Status code:</span> {{status_code}}</p>
        <p><span class="label-bold">Response time:</span> {{response_time}} seconds</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    status_code = None
    response_time = None
    prompt = ""

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        url = "https://jsgbk4z01cvmgz-8000.proxy.runpod.net/generate/line"
        params = {
            "prompt_type": "question",
            "prompt": prompt
        }

        start_time = time.time()
        response = requests.get(url, params=params)
        end_time = time.time()

        status_code = response.status_code
        response_time = round(end_time - start_time, 3)

        if status_code == 200:
            result = response.json()
            response_text = result.get("response", "").strip()
        else:
            response_text = f"Error: {response.text}"

    return render_template_string(HTML, response_text=response_text, status_code=status_code, response_time=response_time, prompt=prompt)

if __name__ == "__main__":
    app.run(debug=True)
