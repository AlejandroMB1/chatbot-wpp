from flask import Blueprint, request
from chatbot_wpp.utils.logging import app_logger
from chatbot_wpp.services.messages import MessagesService


messages_bp = Blueprint("messages", __name__, template_folder="templates", static_folder="static")


class MessagesRoutes:
    def __init__(self, service: MessagesService):
        self.service = service

    def verify_webhook(self):
        app_logger.warning(f"Routes tier -> Webhook verification request received: {request.args}")
        return self.service.verify_webhook(request.args)

    def say_hello(self):
        data = request.get_json()
        app_logger.warning(f"Routes tier -> Webhook received: {data}")
        return self.service.say_hello(data)