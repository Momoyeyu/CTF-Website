#!/bin/bash
# /*%
# *********************************************************
# *功能描述 --%@COMMENT:修改config
# *执行周期 --%@PERIOD:日
# *创建人 --%@CREATOR:mayi
# *创建时间 --%@CREATED_TIME:2020-07-21
# *备注 --%@REMARK:
# **************************************************************
# %*/


echo "Start check `date +'%Y-%m-%d %H:%M:%S'`"

#change max_connections
sed -i 's/max_connections = 100/max_connections = 1000/g' /var/lib/postgresql/data/postgresql.conf

echo "End check `date +'%Y-%m-%d %H:%M:%S'`"
