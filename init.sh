#!/bin/bash

export FLASK_APP=./app.py

pipenv run python dbcreate.py
