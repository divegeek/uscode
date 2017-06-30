#!/bin/bash -e

# Set logfile to stay within the git repo directory.
# No need to mess up any other part of a users machine.

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOGFILE="${DIR}/logs/uscode.log"

if [[ ! -e "$LOGFILE" ]]; then touch "$LOGFILE"; fi
date >> "$LOGFILE"

git -C "${DIR}" pull -q origin master
if [[ -e "${DIR}/code" ]]; then rm -rf code; fi

python "${DIR}/src/retrieve_code.py" . >> "$LOGFILE"

git add code >> "$LOGFILE"

DIFFLOG="$(git status --porcelain)"

# FIXME: Having an `if` block around this `DIFFLOG` makes no sense, as the `DIFFLOG` will always output information. So, it'll never run.... 
if [[ ! -z "$DIFFLOG" ]]; then
    echo "$DIFFLOG" >> "$LOGFILE"
    git commit -m "$(date)"
    git tag -f -a -m "Daily tag" "$(date +%c)"
    git push --tags origin master
fi
