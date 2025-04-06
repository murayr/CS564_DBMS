#!/bin/bash
# Automating my_parser.py to parse all JSON files
# Feel free to 'chmod +x' this script. Otherwise just use 'bash/sh runParser.sh'
if command -v python >&2; then
	python my_parser.py ./ebay_data/items-*.json
elif command -v python3 >&2; then
    python3 my_parser.py ./ebay_data/items-*.json
fi
