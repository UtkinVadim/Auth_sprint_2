from gevent import monkey

from create_admin import create_admin

monkey.patch_all()

import sys

from gevent.pywsgi import WSGIServer

from app import create_app
from config import SERVER_HOST, SERVER_PORT

app = create_app()

if __name__ == "__main__":
    if "-d" in sys.argv:
        app.run(host="0.0.0.0", port=SERVER_PORT, debug=True)
    elif "--create-admin" in sys.argv:
        create_admin(app)
    else:
        http_server = WSGIServer((SERVER_HOST, SERVER_PORT), app)
        http_server.serve_forever()
