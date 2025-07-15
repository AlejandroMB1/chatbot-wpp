from chatbot_wpp.utils.logging import app_logger
from chatbot_wpp.clients.wpp.client import WppClient

SUBSCRIBE_MODE = 'subscribe'


class MessagesService:
    def __init__(self, repository, wpp_client:WppClient):
        self.repository = repository
        self.wpp_client = wpp_client

    def verify_webhook(self, query_params):
        hub_mode = query_params.get('hub.mode')
        hub_challenge = query_params.get('hub.challenge')
        hub_verify_token = query_params.get('hub.verify_token')

        if hub_mode == SUBSCRIBE_MODE and hub_verify_token == self.wpp_client.config.WEBHOOK_VERIFY_TOKEN:
            app_logger.warning("Webhook verified successfully!")
            return hub_challenge, 200
            
        app_logger.warning(f"Webhook verification failed. Token received: '{hub_verify_token}'")
        return "Verification failed", 403

    def say_hello(self, data):
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    # Check if the change is an incoming message notification
                    if value and "messages" in value:
                        metadata = value.get("metadata", {})
                        message = value.get("messages", [{}])[0]

                        from_number = message.get("from")
                        this_number_id = metadata.get("phone_number_id")

                        if from_number and this_number_id:
                            self.wpp_client.send_text_message(this_number_id, from_number, "Hi! I've received your message.")
                    elif value and "statuses" in value:
                        # This is a status update for a message we sent.
                        app_logger.warning(f"Received a status update: {value.get('statuses', [{}])[0]}")

        return "OK", 200
    
