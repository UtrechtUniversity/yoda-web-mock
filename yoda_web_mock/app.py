#!/usr/bin/env python3

__copyright__ = 'Copyright (c) 2023, Utrecht University'
__license__ = 'GPLv3, see LICENSE'

import logging
import os

from flask import Flask, request

from yoda_web_mock.datacite.routes import blueprint_datacite


def create_app() -> Flask:
    logging.basicConfig(filename='mock.log', level=logging.INFO)
    app = Flask(__name__)
    mock_type = os.environ.get("MOCK_TYPE", None)

    if mock_type == "datacite":
        app.register_blueprint(blueprint_datacite)
    elif mock_type is None:
        app.logger.error(
            "Error: no mock type provided. Not loading any blueprint.")
    else:
        app.logger.error(
            f"Error: mock type \"{mock_type}\" not found. " +
            "Not loading any blueprint.")

    @app.before_request
    def log_request_info():
        app.logger.info('Request URL: ' + request.url)
        app.logger.info('Request headers: ' + str(request.headers))
        app.logger.info('Request method: ' + request.method)
        app.logger.info('Request body: ' + str(request.get_data()))
        app.logger.info('End of data for request: ' + request.url)

    return app
