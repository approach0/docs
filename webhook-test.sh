#!/bin/sh
file="webhook-example.json"
url="http://localhost:8080/webhook"

curl -v -H "Content-Type: application/json" -d @"${file}" $url
