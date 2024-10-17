FROM postgres:15-bullseye

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=password
ENV PGDATA=/data/postgres
ENV POSTGRES_DB=message

COPY message.sql .

COPY message.sql /docker-entrypoint-initdb.d/

EXPOSE 5432