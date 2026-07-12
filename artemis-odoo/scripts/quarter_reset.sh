#!/bin/bash

# Artemis Lab - Quarter Reset Script
# Building Intelligent Software, AI & Design Solutions.
# This keeps database backup but resets project/task data
# Use before starting new quarter/batch
# WARNING: This is destructive!

set -e

BACKUP_DIR="/path/to/artemis-odoo/backups"
POSTGRES_CONTAINER="artemis_postgres"
DB_USER="odoo"
DB_NAME="postgres"

echo "=========================================="
echo "Artemis Quarter Reset - DESTRUCTIVE OPERATION"
echo "=========================================="
echo ""
echo "This will:"
echo "1. Create full database backup"
echo "2. Delete all projects, tasks, evaluations"
echo "3. Keep all employees and users"
echo "4. Keep all modules and configurations"
echo ""
read -p "Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

# Step 1: Full Backup
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Creating full backup before reset..."
mkdir -p "$BACKUP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/db_quarter_end_${TIMESTAMP}.sql"

docker exec "$POSTGRES_CONTAINER" pg_dump -U "$DB_USER" "$DB_NAME" > "$BACKUP_FILE"
gzip "$BACKUP_FILE"

if [ -f "${BACKUP_FILE}.gz" ]; then
    echo "[SUCCESS] Backup created: ${BACKUP_FILE}.gz"
else
    echo "[ERROR] Backup failed!"
    exit 1
fi

# Step 2: Reset Data (via SQL)
echo "[INFO] Resetting project data..."

# SQL Script to delete only quarter data
SQL_RESET="
-- Delete tasks first (foreign key dependency)
DELETE FROM project_task WHERE project_id IN (SELECT id FROM project_project WHERE active = true);

-- Delete project milestones (sprints)
DELETE FROM project_milestone WHERE project_id IN (SELECT id FROM project_project WHERE active = true);

-- Delete projects (keep inactive ones for history)
DELETE FROM project_project WHERE active = true;

-- Delete evaluations
DELETE FROM artemis_evaluation;

-- Vacuum database
VACUUM ANALYZE;
"

echo "$SQL_RESET" | docker exec -i "$POSTGRES_CONTAINER" psql -U "$DB_USER" "$DB_NAME"

echo "[SUCCESS] Data reset completed!"
echo "[INFO] All employees, users, and modules remain intact"
echo "[INFO] Ready to create new quarter project"
echo ""
echo "Next steps:"
echo "1. Create new project for new batch"
echo "2. Assign interns to new project"
echo "3. Create new milestones (sprints)"
echo "4. Start assigning tasks"
