#!/usr/bin/env bash
set -eou pipefail
cd "${0%/*}"

[[ -f .env ]] && source .env

source .v/bin/activate

while :; do 
	./newjar.py 2>.newjar.err.log
	sleep .1
done
