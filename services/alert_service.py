import requests
import datetime

# paste your bot token here
BOT_TOKEN = "8761178970:AAGk-hYWpmvCuc8ZOykdg1IZ3AkklrQCS0Y"

# your personal telegram chat id
CHAT_ID = "8623813379"


def send_alert(image_path, confidence):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        "🚨 JetBot Patrol Alert\n\n"
        "Person detected\n\n"
        f"Confidence: {confidence:.2f}\n"
        f"Time: {timestamp}"
    )

    with open(image_path, "rb") as photo:

        requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "caption": message
            },
            files={"photo": photo}
        )