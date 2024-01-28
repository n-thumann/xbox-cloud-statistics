# xbox-cloud-statistics / frontend

## Setup

1. Run `poetry install` to install the dependencies
2. Run `git worktree add ./results origin/results` to checkout the latest results locally
3. Run `python3 -m http.server -d dist/` to start a local HTTP server

## Build

Run `poetry run site-generator` to build the static page.