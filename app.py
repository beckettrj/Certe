from flask import Flask
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Index route hit")
    return "<h1>✅ Certe is deployed! Template test skipped.</h1>"

"""
# All other routes commented out for testing
@app.route('/todays_games')
def todays_games_route():
    ...

# Other routes...
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting app on port {port}")
    app.run(host="0.0.0.0", port=port)