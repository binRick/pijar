#!/usr/bin/env
set -eou pipefail
while :; do
	ssh -TR 127.0.0.1:2223:127.0.0.1:22 $_USER@$_HOST
	sleep 1
done
