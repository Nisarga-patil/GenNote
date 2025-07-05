from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes import bp  # make sure this path is correct based on your structure

import os

# Load environment variables from .env
load_dotenv()

# Create the Flask app
app = Flask(__name__)

# Enable CORS for localhost (dev) and Vercel (prod)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",  # React dev environment
            "http://localhost:3001",  # If you're using port 3001
            "https://gennote.vercel.app",  # your actual Vercel frontend
        ]
    }
})

# Register the blueprint for routes
app.register_blueprint(bp)


# Local development entry point
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
