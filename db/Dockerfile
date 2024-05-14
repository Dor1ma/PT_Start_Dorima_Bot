FROM postgres:14-alpine

ENV POSTGRES_USER=$DB_USER
ENV POSTGRES_PASSWORD=$DB_PASSWORD
ENV POSTGRES_DB=$DB_DATABASE
ENV POSTGRES_HOST_AUTH_METHOD=scram-sha-256
ENV POSTGRES_INITDB_ARGS="--auth-host=scram-sha-256"
ENV POSTGRES_CONFIG="log_replication_commands = on"


COPY ../db/init_01.sql /docker-entrypoint-initdb.d/init_01.sql
