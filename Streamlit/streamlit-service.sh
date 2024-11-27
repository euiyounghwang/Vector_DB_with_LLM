#!/bin/sh
ALERT_SERVICE_ALL_EXPORT_PATH=/home/devuser/rest_api/streamlit
PATH=$PATH:$ALERT_SERVICE_ALL_EXPORT_PATH/bin
SERVICE_NAME=es-alert-service
SERVICE_SUB_NAME=es-alert-ui-service

# See how we were called.
case "$1" in
  start)
        # Start daemon.
        echo "Starting $SERVICE_NAME";
        nohup $ALERT_SERVICE_ALL_EXPORT_PATH/streamlit-ui.sh &> /dev/null &
        #$ALERT_SERVICE_ALL_EXPORT_PATH/alert-ui.sh
        ;;
  stop)
        # Stop daemons.
        echo "Shutting down $SERVICE_NAME";
        pid=`ps ax | grep -i '/streamlit/main.py' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
         else
          echo "$SERVICE_NAME was not Running"
        fi

        echo "Shutting down $SERVICE_SUB_NAME";
        pid=`ps ax | grep -i '/streamlit-ui.sh' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
         else
          echo "$SERVICE_SUB_NAME was not Running"
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        pid=`ps ax | grep -i '/streamlit/main.py' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "$SERVICE_NAME is Running as PID: $pid"
        else
          echo "$SERVICE_NAME is not Running"
        fi

        pid=`ps ax | grep -i '/streamlit-ui.sh' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "$SERVICE_SUB_NAME is Running as PID: $pid"
        else
          echo "$SERVICE_SUB_NAME is not Running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac
~
