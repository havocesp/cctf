#!/usr/bin/env bash
# -------------------------------------------------
# Author:       $Author$
# Created:      $Date$
# Description:  $Description$
# -------------------------------------------------

function cmd_exist() {
    if command -v "${1:-NULL}" &>/dev/null; then
        return 0
    else
        return 1
    fi
}

function git_exists() {
    cmd_exist git
}
function pip_exists() {
    cmd_exist pip"${1:-}"
}
function python3_exists() {
    if cmd_exist python3; then
        python3 -m pip --version
    fi
}

function python_numeric_version() {
    exec 2>&1
    python"${1:-}" -V -V 2>&1 | cut -zc8,10
    exec
}

if git_exists; then
    echo " - [FOUND] git"
    if cmd_exist python3; then
        echo " - [FOUND] python 3"
    elif python_exists && (($(python3 -V 2>&1 | grep -oE '[2-9]' | tr -d '\n') > 350)); then
        echo " - [FOUND] python"
    else
        echo " - [ERROR] git command could not be located please install it and try again."
        exit 1
    fi
else
    echo " - [ERROR] git command could not be located please install it and try again."
    exit 1
fi

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo " - [ERROR] python3 could not be located please install it and try again."
fi

if ! command -v pip3 &>/dev/null && ! command -v pip &>/dev/null; then
    echo " - [ERROR] python3 could not be located please install it and try again."
fi

if [ -d './venv' ] && [ -f './venv/bin/activate' ]; then

    echo "Activating python virtual environment ... "
    source './venv/bin/activate'
fi

echo "Installing dependencies ... "
pip install -U git+https://github.com/havocesp/panance || pip3 install -U git+https://github.com/havocesp/panance
pip install -U git+https://github.com/havocesp/finta || pip3 install -U git+https://github.com/havocesp/finta
pip install -U tabulate || pip3 install -U tabulate
pip install -U defopt || pip3 install -U defopt

echo "Installing clinance ..."
pip install -U . || pip3 install -U .

echo "DONE"
if declare | grep -iq -E ^deactivate; then
    deactivate &>/dev/null
fi
