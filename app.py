import os
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash-lite:generateContent"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat_route():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a question."}), 400

    if not GEMINI_API_KEY:
        app.logger.error("GEMINI_API_KEY is missing.")
        return jsonify({
            "error": "The AI service is not configured yet."
        }), 500

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY
    }

    payload = {
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "You are StudyMate AI, a friendly study assistant "
                        "for college students. Explain concepts in "
                        "beginner-friendly language. Use short steps and "
                        "examples when useful. Keep answers clear and "
                        "well-organized. If you are unsure, say so."
                    )
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": message}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2048
        }
    }

    try:
        response = requests.post(
            GEMINI_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if not response.ok:
            print("Gemini API Error:", response.status_code)
            print("Error Details:", response.text)

            return jsonify({
                "error": (
                    "The AI service could not answer right now. "
                    "Please try again."
                )
            }), 502

        result = response.json()

        candidates = result.get("candidates", [])

        if not candidates:
            return jsonify({
                "error": "The AI could not generate an answer. Please try again."
            }), 502

        parts = candidates[0].get("content", {}).get("parts", [])

        answer = "\n".join(
            part["text"]
            for part in parts
            if "text" in part
        ).strip()

        if not answer:
            return jsonify({
                "error": "The AI returned an empty answer. Please try again."
            }), 502

        return jsonify({"reply": answer})

    except requests.Timeout:
        app.logger.warning("Gemini API request timed out.")

        return jsonify({
            "error": "The AI is taking too long to respond. Please try again."
        }), 504

    except requests.RequestException:
        app.logger.exception("Could not connect to Gemini API.")

        return jsonify({
            "error": "Could not connect to the AI service. Please try again."
        }), 502

    except (ValueError, KeyError, TypeError):
        app.logger.exception("Could not process the Gemini response.")

        return jsonify({
            "error": "Something went wrong while processing the answer."
        }), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)