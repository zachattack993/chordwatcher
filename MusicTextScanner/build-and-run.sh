#!/usr/bin/env bash
set -e
echo "Building Music Text Scanner..."
mvn clean package
echo "Starting app..."
java -jar target/MusicTextScanner-1.0.0.jar
