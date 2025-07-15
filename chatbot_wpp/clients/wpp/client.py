from chatbot_wpp.config import WppConfig
from chatbot_wpp.utils.logging import app_logger
import requests


class WppClient:
    def __init__(self, config:WppConfig):
        self.config = config

    def send_text_message(self, from_id, to_number, message):
        """Sends a message to the WhatsApp API."""

        url = f"{self.config.GRAPH_BASE_URL}{self.config.GRAPH_VERSION}/{from_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.config.META_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to_number,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": message
            }
        }
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            app_logger.warning(f"Message sent to {to_number}, response: {response.json()}")
            return True
        except requests.exceptions.RequestException as e:
            app_logger.error(f"Error sending message to {to_number}: {e}")
            return False