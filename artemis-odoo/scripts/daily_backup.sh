#!/bin/bash

# Artemis Lab - Daily Database Backup Script
# Building Intelligent Software, AI & Design Solutions.
# Run via cron: 0 2 * * * /path/to/artemis-odoo/scripts/daily_backup.sh

set -e

# Configuration
BACKUP_DIR="/path/to/artemis-odoo/backups"
POSTGRES_CONTAINER="artemis_postgres"
DB_USER="artemis"
DB_NAME="artemis_lab"
RETENTION_DAYS=30

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/db_backup_${TIMESTAMP}.sql"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting database backup..."

# Check if container is running
if ! docker ps | grep -q "$POSTGRES_CONTAINER"; then
    echo "[ERROR] PostgreSQL container ($POSTGRES_CONTAINER) is not running!"
    exit 1
fi

# Perform backup
docker exec "$POSTGRES_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"

if [ -f "$BACKUP_FILE" ]; then
    SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "[SUCCESS] Database backed up to: $BACKUP_FILE (Size: $SIZE)"
    
    # Compress backup
    gzip "$BACKUP_FILE"
    echo "[INFO] Backup compressed: ${BACKUP_FILE}.gz"
else
    echo "[ERROR] Backup file not created!"
    exit 1
fi

# Delete old backups (older than RETENTION_DAYS)
echo "[INFO] Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "db_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup completed successfully!"
