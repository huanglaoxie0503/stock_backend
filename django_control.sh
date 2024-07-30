#!/bin/bash

# 定义 Conda 虚拟环境的名称
CONDA_ENV="backend"

# 激活 Conda 虚拟环境
source /home/picker/miniconda3/bin/activate $CONDA_ENV

# 定义 Django 项目的路径和启动命令
PROJECT_DIR="/home/picker/projects/stock_backend"
START_COMMAND="python manage.py runserver 0.0.0.0:8080"

# 检查 Django 项目是否在运行中
is_running() {
    pgrep -f "$START_COMMAND" > /dev/null
    return $?
}

# 启动 Django 项目
start() {
    is_running
    if [ $? -eq 0 ]; then
        echo "Django project is already running."
    else
        echo "Starting Django project..."
        cd $PROJECT_DIR
        nohup $START_COMMAND &
        echo "Django project started."
    fi
}

# 停止 Django 项目
stop() {
    is_running
    if [ $? -eq 0 ]; then
        echo "Stopping Django project..."
        pkill -f "$START_COMMAND"
        echo "Django project stopped."
    else
        echo "Django project is not running."
    fi
}
# 检查参数并执行相应操作
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
        is_running
        if [ $? -eq 0 ]; then
            echo "Django project is running."
        else
            echo "Django project is not running."
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

# 退出 Conda 虚拟环境
conda deactivate

exit 0

