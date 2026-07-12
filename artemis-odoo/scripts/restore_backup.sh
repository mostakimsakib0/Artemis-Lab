#!/bin/bash

# Artemis Lab - Restore Database from Backup
# Building Intelligent Software, AI & Design Solutions.
# Usage: ./restore_backup.sh <backup_file>
# Example: ./restore_backup.sh backups/db_backup_20250115_020000.sql.gz

set -e

BACKUP_FILE="$1"
POSTGRES_CONTAINER="artemis_postgres"
DB_USER="artemis"
DB_NAME="artemis_lab"

# Validation
if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    echo "Example: $0 backups/db_backup_20250115_020000.sql.gz"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "[ERROR] Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "[WARNING] This will overwrite the current database!"
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting database restore..."

# Stop Odoo (keep postgres running)
echo "[INFO] Stopping Odoo container..."
docker-compose down --remove-orphans

echo "[INFO] Waiting for postgres to be ready..."
sleep 3

# Decompress if needed
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo "[INFO] Decompressing backup..."
    TEMP_FILE="${BACKUP_FILE%.gz}"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    RESTORE_FILE="$TEMP_FILE"
else
    RESTORE_FILE="$BACKUP_FILE"
fi

# Start postgres container to perform restore
docker-compose up -d db

echo "[INFO] Waiting for postgres service..."
sleep 5

# Restore database
echo "[INFO] Restoring database from $RESTORE_FILE..."
docker exec -i "$POSTGRES_CONTAINER" psql -U "$DB_USER" "$DB_NAME" < "$RESTORE_FILE"

if [ $? -eq 0 ]; then
    echo "[SUCCESS] Database restored successfully!"
else
    echo "[ERROR] Database restore failed!"
    exit 1
fi

# Cleanup temp file if it was decompressed
if [[ "$BACKUP_FILE" == *.gz ]] && [ -f "$TEMP_FILE" ]; then
    rm "$TEMP_FILE"
fi

# Start all services
echo "[INFO] Starting all services..."
docker-compose up -d

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restore completed. Odoo will be available at port 8069."
