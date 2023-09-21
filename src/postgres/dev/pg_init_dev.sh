#!/bin/bash

########################################################################
#
# pg init dev sh
#
########################################################################


db_host=localhost
db_name=pingpong-match
db_user=postgres
db_pass=postgres
db_port=5432

psqlWhich=$(dirname `which psql`)
HANDSQL="$psqlWhich/psql -U ${db_user} -d ${db_name} -h ${db_host} -p ${db_port}"
ADMINSQL="$psqlWhich/psql -U ${db_user} -d postgres -h ${db_host} -p ${db_port}"
CREATEDBSQL="$psqlWhich/createdb ${db_name} -U ${db_user} -h ${db_host} -p ${db_port} -e"

export PGPASSWORD=${db_pass}

function init_env {
    #脚本名，去.sh后缀
    SCRIPT_NAME="$(basename $0 .sh)"
    #脚本安装路径
    DIR_INSTALL=$(cd $(dirname $0);pwd)
    #脚本运行日期
    DAY=$(date +'%Y%m%d')
    HOUR=$(date +'%H')
    TIME=$(date +'%H%M%S')
    #日志目录路径
    DIR_LOG="${DIR_INSTALL}/logs/"
    #脚本运行正常日志
    LOG_NORMAL="${DIR_LOG}/${SCRIPT_NAME}_${DAY}.log"
    #脚本运行错误日志
    LOG_ERROR="${DIR_LOG}/${SCRIPT_NAME}_${DAY}.err"
    #建立日志存放目录
    mkdir -p ${DIR_LOG}
    #exec 2>"${LOG_ERROR}"
}

function import_init_sql {
    sqlFile=$1

    echo "IMPORT $sqlFile"
    ${HANDSQL} -f ${DIR_INSTALL}/../$sqlFile
}

function import_init_csv {
    schemaName=$1
    tableName=$2

    echo "\COPY $schemaName.$tableName FROM '$schemaName.$tableName.csv' WITH CSV HEADER"
    ${HANDSQL} -c "\COPY $schemaName.$tableName FROM '${DIR_INSTALL}/../csv/$schemaName.$tableName.csv' WITH CSV HEADER"
}

function echo_db_info {
    echo [INFO] ${db_host}:${db_port}/${db_name}
}

function create_db {
    dbExist=`${ADMINSQL} -t -c "select datname from pg_database where datname='${db_name}'"`
    if [ "$dbExist" != "" ]; then
        echo $dbExist exists.
        echo -n "Do you confirm to drop database ${db_name} (*required) ? [Y|N] "
        read CONFIRM_DROP
        case $CONFIRM_DROP in
        y|Y|yes|Yes|YES)
            echo "Confirmed."
            ;;
        *)
            echo Cancel to exit!
            exit
            ;;
        esac

        echo "Disconnect ${db_name}"
        ${ADMINSQL} -c "select pg_terminate_backend(pid) from pg_stat_activity where datname='${db_name}'"
        echo "Disconnect ${db_name}"
        ${ADMINSQL} -c "drop database \"${db_name}\""
    fi

    ${CREATEDBSQL}
    ${HANDSQL} -c "create language plpgsql"
}

function check_plpgsql_language {
    languageExist=`${HANDSQL} -t -c "select lanname from pg_language where lanname='plpgsql'"`
    if [ "$languageExist" = "" ]; then
        echo "CREATE LANGUAGE plpgsql;"
        ${HANDSQL} -c "CREATE LANGUAGE plpgsql;"
    fi
}

init_env
echo_db_info

check_plpgsql_language
create_db

import_init_sql init_journal.sql
import_init_sql init_auth.sql
import_init_sql init_public.sql

import_init_csv auth group
import_init_csv auth user
import_init_csv auth user_group
import_init_csv auth menu
import_init_csv auth group_menu

# 导入数据后，重设id seq
import_init_sql id_seq_reset.sql

echo [Finished]
