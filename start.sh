#!/usr/bin/env sh

DEV_MODE=${DEV_MODE:-false}

rm -rf venv

python3 -m venv venv

. venv/bin/activate && \
pip install --upgrade pip && \
pip install -r requirements.txt

chown -R 1000:1000 venv

python3 app.py
