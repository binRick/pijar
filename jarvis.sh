#!/usr/bin/env bash
set -eou pipefail
cd "${0%/*}"

[[ -f .env ]] && source .env

source .v/bin/activate

while :; do 
	./jarvis.py 2>/dev/null
	sleep .1
done
