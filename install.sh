#!/bin/bash
#
# Simple script to install freespace-notify from the master branch

set -e

HOME_BIN="$HOME/bin";
SCRIPT_NAME="freespace-notify.py"
SCRIPT_URL="https://raw.githubusercontent.com/mauro-bytelion/freespace-notify/master/$SCRIPT_NAME";
SCRIPT_PATH="$HOME_BIN/$SCRIPT_NAME";

# first create the ~/bin dir
if [ ! -d "$HOME_BIN" ];
then
    echo "[*] Creating ~/bin directory...\n";
    mkdir -p "$HOME_BIN";
fi;

# then check if freespace-notify is there, and it's executable.
if [ ! -x "$SCRIPT_PATH" ];
then
    echo "[*] Installing freespace-notify.py...\n";
    wget $SCRIPT_URL -O $SCRIPT_PATH > /dev/null 2>&1;
    chmod +x $SCRIPT_PATH;
fi;

# and that's all :-)
echo "********************************"
echo "          All done!             "
echo "freespace-notify.py is installed"
echo "********************************"
exit 0
