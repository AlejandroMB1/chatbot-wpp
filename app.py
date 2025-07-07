from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import json
import requests

SUBSCRIBE_MODE = 'subscribe'

load_dotenv()
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
ACCESS_TOKEN = os.environ.get('META_ACCESS_TOKEN')

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/webhooks', methods=['GET'])
def verify_webhook():
	app.logger.info(f"Webhook verification request received: {request.args}")
	hub_mode = request.args.get('hub.mode')
	hub_challenge = request.args.get('hub.challenge')
	hub_verify_token = request.args.get('hub.verify_token')

	if hub_mode == SUBSCRIBE_MODE and hub_verify_token == VERIFY_TOKEN:
			app.logger.info("Webhook verified successfully!")
			return hub_challenge, 200
		
	app.logger.warning(f"Webhook verification failed. Token received: '{hub_verify_token}'")
	return "Verification failed", 403

def send_whatsapp_message(from_id, to_number, message):
	"""Sends a message to the WhatsApp API."""
	url = f"https://graph.facebook.com/v22.0/{from_id}/messages"
	headers = {
		"Authorization": f"Bearer {ACCESS_TOKEN}",
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
		app.logger.info(f"Message sent to {to_number}, response: {response.json()}")
		return True
	except requests.exceptions.RequestException as e:
		app.logger.error(f"Error sending message to {to_number}: {e}")
		return False


@app.route('/webhooks', methods=['POST'])
def receive_webhook():
	data = request.get_json()
	app.logger.info(f"Webhook received: {data}")
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
						send_whatsapp_message(this_number_id, from_number, "Hi! I've received your message.")
				elif value and "statuses" in value:
					# This is a status update for a message we sent.
					app.logger.info(f"Received a status update: {value.get('statuses', [{}])[0]}")

	# Meta requires a 200 OK response to prevent webhook disabling.
	return "OK", 200

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)