from flask import Flask
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("✅ Index route was hit")
    return "<h1>✅ Certe is finally LIVE!</h1><BR><H2> test 123</H2>"
    
def favicon():
    return '', 204

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logging.info(f"Starting app on port {port}")
    app.run(host="0.0.0.0", port=port)  
