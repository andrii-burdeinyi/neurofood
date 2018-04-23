#!/usr/bin/env sh

DEV_MODE=${DEV_MODE:-false}

if [ ${DEV_MODE} = true ]; then
    if [ -d "venv" ]; then
        rm -rf venv
    fi

    python3 -m venv venv

    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt
fi

python3 run.py
