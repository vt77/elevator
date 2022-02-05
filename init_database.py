#!/usr/bin/python3

import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()

from storage.sqlite import init_database
init_database('./app.db')

