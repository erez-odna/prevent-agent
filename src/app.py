from flask import Flask
from settings import AppSettings
from endpoints.post import post_blueprint


AppSettings.loadenv()

app = Flask(__name__)

# register blueprints
app.register_blueprint(post_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
