from flask import Flask, render_template
from chatbot_wpp.config import config
from chatbot_wpp.clients.wpp.client import WppClient
from chatbot_wpp.services.messages import MessagesService
from chatbot_wpp.modules.messages.routes import MessagesRoutes, messages_bp


def create_app(config_name="dev"):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	wpp_config = app.config.get('WPP_CONFIG')

	# Check for required environment variables
	required_vars = {
		'WEBHOOK_VERIFY_TOKEN': wpp_config.WEBHOOK_VERIFY_TOKEN,
		'META_ACCESS_TOKEN': wpp_config.META_ACCESS_TOKEN,
		'GRAPH_BASE_URL': wpp_config.GRAPH_BASE_URL,
		'GRAPH_VERSION': wpp_config.GRAPH_VERSION
	}

	missing_vars = [key for key, val in required_vars.items() if val is None]
	if missing_vars:
		raise ValueError(f"CRITICAL: Missing environment variables: {missing_vars}.")

	wpp_client = WppClient(wpp_config)
	# Messages routes
	msgs_service = MessagesService(None, wpp_client)
	msgs_router = MessagesRoutes(msgs_service)
	messages_bp.add_url_rule("/webhooks", view_func=msgs_router.verify_webhook, methods=['GET'])
	messages_bp.add_url_rule("/webhooks", view_func=msgs_router.say_hello, methods=['POST'])

	app.register_blueprint(messages_bp)

	@app.route("/")
	def index():
		return render_template("index.html")

	return app