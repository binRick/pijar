#!/usr/bin/env bash
set -eou pipefail
cd "${0%/*}"

[[ -f .env ]] && source .env

source .v/bin/activate

while :; do 
	./jarvis.py
	sleep .1
done
