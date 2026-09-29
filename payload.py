import requests

WEBHOOK_URL = "http://localhost:5000/webhook"
SENDER_ID = "1234567890"


def send_message(message_text):
    payload = {
        "object": "page",
        "entry": [{
            "messaging": [{
                "sender": {"id": SENDER_ID},
                "message": {"text": message_text}
            }]
        }]
    }

    response = requests.post(
        WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=10,
    )

    print(f"Sent: {message_text}")
    print(f"Status: {response.status_code}")
    print(response.text)


if __name__ == "__main__":
    while True:
        message_text = input("Enter message (or 'exit' to quit): ").strip()

        if message_text.lower() == "exit":
            print("Exiting loop...")
            break

        if not message_text:
            print("Message cannot be empty.")
            continue

        send_message(message_text)