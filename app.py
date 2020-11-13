# -*- coding: utf-8 -*-
from chalice import Chalice

import sys
import json
import logging
import os
import time
from datetime import date, datetime, timedelta


app = Chalice(app_name='StockAlarm')


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/meta')
def call_meta():
    return app.current_request.to_dict()


@app.route('/readme')
def call_meta():
    # TODO write markdown..
    markdown = ''
    return markdown
