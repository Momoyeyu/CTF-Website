
FROM postgres:12.1-alpine

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB pingpong-match

ENV WORK_DIR /opt/pingpong-match/db

RUN mkdir -p $WORK_DIR
RUN mkdir -p $WORK_DIR/csv

# 同步系统时间
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

COPY csv/* $WORK_DIR/csv/
COPY init_*.sql $WORK_DIR/
COPY id_seq_reset.sql $WORK_DIR/

COPY conn_change.sh /docker-entrypoint-initdb.d/
COPY docker_init_db.sql /docker-entrypoint-initdb.d/

# [build]
# # 如果正式push到harbor，需在服务器上进行build，mac M1/M2芯片build后服务器运行报错
# docker build -t harbor.lab.bigai.site/pingpong-match/pingpong-match-postgres:1.0.0 .
# docker images | grep pingpong-match-postgres

# [run] create+start
# docker stop pingpong-match-postgres && docker rm pingpong-match-postgres
# docker run --name pingpong-match-postgres -p 15432:5432 -itd harbor.lab.bigai.site/pingpong-match/pingpong-match-postgres:1.0.0

# [exec]
# docker exec -it pingpong-match-postgres sh
# docker exec -it pingpong-match-postgres psql -U postgres pingpong-match -c 'select version()'

# [logs]
# docker logs pingpong-match-postgres

# [push]
# docker push harbor.lab.bigai.site/pingpong-match/pingpong-match-postgres:1.0.0

# [remove]
# docker stop pingpong-match-postgres && docker rm pingpong-match-postgres
