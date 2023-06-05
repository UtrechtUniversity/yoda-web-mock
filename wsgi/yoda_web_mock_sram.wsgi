#!/usr/bin/env python3

import os
import sys

activate_this = '/var/www/webmock/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from yoda_web_mock import app

os.environ["MOCK_TYPE"]="sram"
os.environ["LOGFILE"]="/var/www/webmock/log/mock-sram.log"
application = app.create_app()
