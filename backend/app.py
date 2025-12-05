from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
CORS(app)

from app.routes import api

app.register_blueprint(api, url_prefix="/")

@app.route("/")
def home():
    return {"message": "Hello, Flask is running!"}

if __name__ == "__main__":
    app.run(debug=True)
