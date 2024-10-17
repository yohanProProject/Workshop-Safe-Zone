# app.py

from api.message.message import messages_root
from api.message.level import levels_root
from api.message.platform import platforms_root
from api.message.harassment_type import harassment_types_root
from api.database.connection_db import app
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import os

load_dotenv()

CORS(app)

# Route principale
@app.route('/')
def hello_world():
    return 'Hello, World!'

app.register_blueprint(messages_root, url_prefix='/message')
app.register_blueprint(levels_root, url_prefix="/level")
app.register_blueprint(platforms_root, url_prefix="/platform")
app.register_blueprint(harassment_types_root, url_prefix="/harassment_type")

if __name__ == '__main__':
    app.run(debug=True, host=os.getenv("HOST"), port=os.getenv("PORT"))