# gunicorn/django  服务监听地址、端口
bind = '0.0.0.0:8000'

# gunicorn worker 进程个数，建议为： CPU核心个数 * 2 + 1
workers =  4

# gunicorn worker 类型， 使用异步的event类型IO效率比较高
worker_class =  "gevent"

# 日志文件路径
errorlog = "/usr/src/app/gunicorn.log"
loglevel = "info"

import sys,os

cwd = os.getcwd()
sys.path.append(cwd)