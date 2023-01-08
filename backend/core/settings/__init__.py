import platform
from .base import *
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()


os_type = platform.system()

if os_type == 'Windows':
    print('进入 dev ')
    from .dev import *
elif os_type == 'Linux':
    print('进入 prod ')
    from .prod import *
else:
    print('进入 mac')
    from .mac import *
