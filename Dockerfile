FROM alpine:latest

# Install SQLite
RUN apk add --no-cache sqlite

WORKDIR /

# Copy an optional init script to set up the database
COPY init-db.sql ./init-db.sql

VOLUME /db

# Run SQLite with an interactive shell or execute the init script
CMD ["sh", "-c", "sqlite3 /db/mydb.db < /init-db.sql && sqlite3 /db/mydb.db"]
