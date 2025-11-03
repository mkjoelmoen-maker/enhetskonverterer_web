#!/bin/bash

# Sett port fra miljøvariabel, fallback til 5000 hvis ikke satt
PORT=${PORT:-5000}

# Start Flask-appen med gunicorn
gunicorn app:app --bind 0.0.0.0:$PORT


