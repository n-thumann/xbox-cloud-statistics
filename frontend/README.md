# xbox-cloud-statistics / frontend

## Setup

1. Run `poetry install` to install the dependencies
2. Download https://github.com/n-thumann/xbox-cloud-statistics/releases/download/results/results.tar.gz and extract it to get latest results locally
3. Run `python3 -m http.server -d dist/` to start a local HTTP server

## Build

Run `poetry run site-generator` to build the static page.