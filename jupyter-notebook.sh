#!/bin/bash
set -e

#JUPYTER_NOTEBOOK_PATH=/home/devuser/monitoring/jupyter_notebook
#PATH=$PATH:$JUPYTER_NOTEBOOK_PATH
#SERVICE_NAME=jupyter-notebook-service-all-service

# -- enable jdk11 for h2/disable jdk11 path for oracle
#JAVA_HOME=~/monitoring/openlogic-openjdk-11.0.23+9-linux-x64/
#export PATH=$JAVA_HOME/bin:$PATH
#export JAVA_HOME

export PYTHONDONTWRITEBYTECODE=1

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

VENV=".venv"

# Python 3.11.7 with Window
if [ -d "$VENV/bin" ]; then
    source $SCRIPTDIR/$VENV/bin/activate
else
    source $SCRIPTDIR/$VENV/Scripts/activate
fi

# pip install jupyterlab

#jupyter notebook
# jupyter lab


export SMTP_HOST="test.com"
export SMTP_PORT=25
export MAIL_SENDER="es-report@test.com"
export MAIL_USERLIST="test@test.com"
export MAIL_CC="testg@test.com"


#jupyter notebook
#jupyter lab


# See how we were called.
case "$1" in
  start)
        # Start daemon.
        echo "Starting $SERVICE_NAME";
        # nohup jupyter lab --ip 0.0.0.0 &> /dev/null &
        jupyter lab --ip 0.0.0.0 --port=8889
        ;;
  stop)
        # Stop daemons.
        echo "Shutting down $SERVICE_NAME";
        pid=`ps ax | grep -i '/jupyter-lab' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
         else
          echo "$SERVICE_NAME was not Running"
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        pid=`ps ax | grep -i '/jupyter-notebook' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "$SERVICE_NAME is Running as PID: $pid"
        else
          echo "$SERVICE_NAME is not Running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac


