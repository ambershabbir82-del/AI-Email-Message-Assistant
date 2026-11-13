"""app.py - Flask server: serves the page and exposes POST /generate."""
from flask import Flask, jsonify, render_template, request

from groq_service import GroqServiceError, generate_message
from prompts import MESSAGE_TYPE_LIST, TONE_LIST, build_prompt

app = Flask(__name__)

MAX_LENGTH = 3000


@app.route("/")
def index():
    return render_template("index.html", message_types=MESSAGE_TYPE_LIST, tones=TONE_LIST)


def fail(message, status):
    return jsonify({"success": False, "generated_message": "", "error": message}), status


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return fail("Invalid request. Please try again.", 400)

    message = str(data.get("message", "")).strip()
    message_type = str(data.get("message_type", "")).strip()
    tone = str(data.get("tone", "")).strip()

    # Validation with if / elif
    if not message:
        return fail("Please enter your message.", 400)
    elif len(message) > MAX_LENGTH:
        return fail(f"Your message is too long. Keep it under {MAX_LENGTH} characters.", 400)
    elif message_type not in MESSAGE_TYPE_LIST:
        return fail("Please select a valid message type.", 400)
    elif tone not in TONE_LIST:
        return fail("Please select a valid writing tone.", 400)

    prompt = build_prompt(message, message_type, tone)

    try:
        result = generate_message(prompt)
    except GroqServiceError as error:
        return fail(str(error), 502)
    except Exception:
        return fail("Something went wrong. Please try again.", 500)

    return jsonify({"success": True, "generated_message": result})


if __name__ == "__main__":
    app.run(debug=True)
