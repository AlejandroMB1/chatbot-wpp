import os
from dotenv import load_dotenv

load_dotenv()

class WppConfig:
    WEBHOOK_VERIFY_TOKEN = os.environ.get('WEBHOOK_VERIFY_TOKEN')
    META_ACCESS_TOKEN = os.environ.get('META_ACCESS_TOKEN')
    GRAPH_BASE_URL = os.environ.get('GRAPH_BASE_URL')
    GRAPH_VERSION = os.environ.get('GRAPH_VERSION')


class Config:
    WPP_CONFIG = WppConfig()


config = {
    "dev": Config
}