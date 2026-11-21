
from flask import Flask, render_template, request, jsonify
from ollama import chat

app = Flask(__name__)

MODEL = "llama3.2:1b"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat_route():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a friendly study assistant for college students. "
                    "Explain concepts in simple language. "
                    "Keep answers short and clear. "
                    "Use examples when helpful. "
                    "Limit most answers to around 100 words."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        options={
            "num_predict": 150,
        },
    )
        answer = response.message.content or "I couldn't generate a response."

        return jsonify({"reply": answer})

    except Exception:
        app.logger.exception("Ollama request failed")

        return jsonify({
            "error": (
                "Could not connect to Ollama. "
                "Make sure Ollama is running and the model is installed."
            )
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port="5000" , debug=True)
