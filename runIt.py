import os
import time

import requests
from requests.exceptions import ConnectionError

from webApp import app, db

if __name__ == "__main__":
    esUrl = os.environ.get("FLASK_FORUM_ES_URL")

    # wait for elasticsearch service to be ready before starting server

    print(f"waiting for elasticsearch service to be ready by querying {esUrl}...")

    while True:
        try:
            time.sleep(2)
            elasticRequest = requests.get(f"http://{esUrl}")
            if elasticRequest.status_code >= 200 and elasticRequest.status_code < 500:
                break
        except ConnectionError:
            pass

    print("elasticsearch ready, creating database schema...")

    db.create_all()

    print("database schema created, running server...")

    app.run(host="0.0.0.0", debug=True)
