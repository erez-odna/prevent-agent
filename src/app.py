from flask import Flask
from flask_cors import CORS
import serverless_wsgi
from settings import AppSettings
from endpoints.post import post_blueprint


AppSettings.loadenv()

app = Flask(__name__)
CORS(app)

# register blueprints
app.register_blueprint(post_blueprint)


def main_handler(event, context):
    print("main_handler")
    if "httpMethod" in event or "headers" in event:
        print("detected API Gateway event → routing to Flask app")
        return serverless_wsgi.handle_request(app, event, context)

    if "triggerSource" in event:
        print(f"found triggerSource {event['triggerSource']}")
        return handle_cognito_triggered_event(event)

    if "command" in event:
        print("command in event")
    print(
        "neither command nor triggerSource nor http request data is present in event, exiting"
    )
    print(event)
    return event


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50)
