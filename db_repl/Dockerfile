FROM postgres:14-alpine

ENV POSTGRES_USER=replicator
ENV POSTGRES_PASSWORD=replicator_password
ENV POSTGRES_DB=postgres
ENV POSTGRES_HOST=postgres_primary

RUN echo "#!/bin/bash" > /init.sh && \
    echo "rm -rf /var/lib/postgresql/data/*" >> /init.sh && \
    echo "until PGPASSWORD=$POSTGRES_PASSWORD pg_basebackup --pgdata=/var/lib/postgresql/data -R --slot=replication_slot --username=$POSTGRES_USER --host=postgres_primary --port=5432; do" >> /init.sh && \
    echo "  echo 'Waiting for primary to connect...'" >> /init.sh && \
    echo "  sleep 1s" >> /init.sh && \
    echo "done" >> /init.sh && \
    echo "echo 'Backup done, starting replica...'" >> /init.sh && \
    echo "chmod 0700 /var/lib/postgresql/data" >> /init.sh && \
    echo "psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -c \"SELECT * FROM pg_create_physical_replication_slot('replication_slot');\"" >> /init.sh && \
    echo "postgres" >> /init.sh

RUN chmod +x /init.sh

USER postgres

CMD ["/init.sh"]
