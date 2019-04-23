#!/usr/bin/env bash
#
# e: Exit immediately on fail
# E: Inherit ERR trap so it works correctly if something fails and we exit because of -e
# u: Treat unset variables as errors
# x: Print each instruction to stderr before executing
# o pipefail: Exit status of pipe is non-zero if any step in pipe fails
set -Eeuxo pipefail

if [[ -z "${STAGE+x}" ]]; then
	export MYPYPATH="./stubs"
else
	export MYPYPATH="${MYPYPATH}:./stubs"
fi

for file in ./*.py; do
	eval "python3 -m mypy ${file}"
done
