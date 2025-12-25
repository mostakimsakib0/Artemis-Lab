#!/bin/bash

# MIU Software R&D Lab - Health Check Script
# Run periodically to ensure all services are healthy
# Usage: ./health_check.sh

set -e

ODOO_CONTAINER="miu_odoo"
POSTGRES_CONTAINER="miu_postgres"
ODOO_PORT=8069
POSTGRES_PORT=5432

echo "=========================================="
echo "MIU System Health Check"
echo "$(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

HEALTH_STATUS=0

# Check 1: Docker containers running
echo -n "[CHECK 1] Docker containers running... "
if docker ps | grep -q "$ODOO_CONTAINER" && docker ps | grep -q "$POSTGRES_CONTAINER"; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    HEALTH_STATUS=1
fi

# Check 2: PostgreSQL connectivity
echo -n "[CHECK 2] PostgreSQL connectivity... "
if docker exec "$POSTGRES_CONTAINER" psql -U odoo postgres -c "SELECT 1" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    HEALTH_STATUS=1
fi

# Check 3: Odoo HTTP response
echo -n "[CHECK 3] Odoo HTTP port ($ODOO_PORT)... "
if timeout 5 bash -c "echo > /dev/tcp/localhost/$ODOO_PORT" 2>/dev/null; then
    echo -e "${GREEN}✓ OK${NC}"
else
    echo -e "${RED}✗ FAILED${NC}"
    HEALTH_STATUS=1
fi

# Check 4: Database size
echo -n "[CHECK 4] Database size... "
DB_SIZE=$(docker exec "$POSTGRES_CONTAINER" psql -U odoo postgres -t -c "SELECT pg_size_pretty(pg_database_size('postgres'))")
echo -e "${GREEN}$DB_SIZE${NC}"

# Check 5: Disk space
echo -n "[CHECK 5] Disk space... "
DISK_USAGE=$(docker exec "$ODOO_CONTAINER" df -h /var/lib/odoo | tail -1 | awk '{print $5}')
if [ "${DISK_USAGE%\%}" -gt 80 ]; then
    echo -e "${YELLOW}⚠ WARNING: $DISK_USAGE used${NC}"
else
    echo -e "${GREEN}✓ OK ($DISK_USAGE)${NC}"
fi

# Check 6: Recent errors
echo -n "[CHECK 6] Recent Odoo errors... "
ERROR_COUNT=$(docker logs --tail 100 "$ODOO_CONTAINER" 2>&1 | grep -c "ERROR" || true)
if [ "$ERROR_COUNT" -gt 5 ]; then
    echo -e "${YELLOW}⚠ $ERROR_COUNT errors found${NC}"
else
    echo -e "${GREEN}✓ OK${NC}"
fi

echo ""
echo "=========================================="
if [ $HEALTH_STATUS -eq 0 ]; then
    echo -e "${GREEN}✓ System Health: GOOD${NC}"
else
    echo -e "${RED}✗ System Health: ISSUES DETECTED${NC}"
fi
echo "=========================================="

exit $HEALTH_STATUS
