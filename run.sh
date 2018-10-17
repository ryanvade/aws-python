#!/bin/bash
FLASK_APP=src/index.py pipenv run aws-vault exec personal -- flask run
