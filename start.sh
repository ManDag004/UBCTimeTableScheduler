#!/bin/bash

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start Python backend
cd tt_scheduler_backend
python3 manage.py runserver &
cd ..

# Setup React environment
cd tt-scheduler-frontend
npm install

# Start React frontend
npm start
