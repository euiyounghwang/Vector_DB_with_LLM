#!/bin/bash
set -e


SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $SCRIPTDIR
cd ..

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $VENV/bin/activate
else
    source $VENV/Scripts/activate
fi


# streamlit run [streamlit-filenam.py] [--server.port 30001]
# streamlit run $SCRIPTDIR/Streamlit_Chat.py --server.port 7002
streamlit run $SCRIPTDIR/Streamlit_SimpleChat.py --server.port 7002
#streamlit run $SCRIPTDIR/Streamlit_Chat.py
