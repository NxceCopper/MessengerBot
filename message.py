from flask import Flask, request
import re
import os

app = Flask(__name__)
VERIFY_TOKEN = "bed_shop_verify_123"

INTENTS = {
    "price": ["magkano", "presyo", "how much", "price", "cost"],
    "delivery": ["deliver", "cod", "shipping", "pwede ba sa"],
    "size": ["size", "sizes", "queen", "king", "single", "double"],
    "payment": ["installment", "hulugan", "gcash", "bank transfer"],
}

REPLIES = {
    "price": "Our beds range from ₱X,XXX to ₱XX,XXX depending on size.",
    "delivery": "Yes, we deliver! COD available in most areas.",
    "size": "We have Single, Double, Queen, and King sizes.",
    "payment": "We accept GCash, bank transfer, and installment plans.",
}

def find_matched_intents(message: str) -> list[str]:
    message = message.lower()
    matched = []
    for intent, keywords in INTENTS.items():
        for kw in keywords:
            pattern = r"\b" + re.escape(kw) + r"\b"
            if re.search(pattern, message):
                matched.append(intent)
                break
    return matched

def build_reply(matched_intents: list[str]):
    if not matched_intents:
        return None
    return "\n".join(REPLIES[i] for i in matched_intents)

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        return "Verification failed", 403
    return "Invalid request", 400

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message") and "text" in messaging_event["message"]:
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"]["text"]

                    matched = find_matched_intents(message_text)
                    reply = build_reply(matched)
                    if reply is None:
                        reply = "Thanks for your message! Let me have the seller get back to you shortly"

                    print(f"[Message sent to {sender_id}]: {reply}")
        return "EVENT_RECEIVED", 200
    return "Not found", 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)