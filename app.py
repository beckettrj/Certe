import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Railway111!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    print("🟢 Flask running on port:", port)  # Debug log for Railway
    app.run(host='0.0.0.0', port=port)

