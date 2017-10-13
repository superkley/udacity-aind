#!/usr/bin/env bash
export FLASK_APP=autoapp.py
export FLASK_DEBUG=1

source .venv/bin/activate

flask run
