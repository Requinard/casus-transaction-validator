#!/bin/bash

echo "Creating lambda package for App"
cp -r app app-build
cd app-build

echo "Installing requirements into app directory"
poetry export -f requirements.txt > requirements.txt
pip install -r requirements.txt --quiet -t .
chmod -R 755 .

echo "Zipping files"
zip -q -r ../app.zip -7 .

echo "Removing build directory"
cd ..
rm -rf app-build

echo "All done: See app.zip"
