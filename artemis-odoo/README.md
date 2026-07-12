# Artemis Lab - Odoo Setup

> **Building Intelligent Software, AI & Design Solutions.**

Complete production-ready setup for real software company.

**Services:** Software Development · AI Solutions · R&D · Interior Design & 3D Visualization · Automation · Cloud & DevOps

---

## Quick Start (2 minutes)

```bash
cd artemis-odoo
docker-compose up -d
# Wait 30 seconds for services to start
# Visit: http://localhost:8069
```

---

## What's Included

✅ **Docker Setup** - Odoo 17 + PostgreSQL 14  
✅ **Custom Module** - Projects, tasks, evaluations, automation  
✅ **User Roles** - 9 group types (Intern, Developer, Designer, AI Engineer, Tech Lead, PM, QA, CEO, Admin)  
✅ **Automation** - Deadline rejection, PR validation, review requirement  
✅ **Backup Scripts** - Daily backup, restore, quarter reset  
✅ **Complete Documentation** - Setup guide + deployment checklist  

---

## Folder Structure

```
artemis-odoo/
├── docker-compose.yml          # Docker services config
├── SETUP_GUIDE.md              # 15-step complete guide
├── DEPLOYMENT_CHECKLIST.md     # 7-day deployment plan
├── odoo/
│   ├── config/odoo.conf        # Odoo server config
│   ├── addons/artemis_custom/      # Custom module (all features)
│   └── data/                   # Runtime data
├── postgres/data/              # Database (auto-created)
├── backups/                    # Backups folder
└── scripts/
    ├── daily_backup.sh         # Auto-backup
    ├── restore_backup.sh       # Restore from backup
    ├── quarter_reset.sh       # Reset data for next batch
    └── health_check.sh         # System health monitor
```

---

## Core Features

### 1. Project Management
- Projects with milestones (sprints)
- Tasks with dependencies
- GitHub PR integration
- Custom task stages

### 2. User System
- 7 role-based groups
- Intern/CEO/Admin profiles
- Employee skills & batch tracking
- Permission-based access

### 3. Automation
- **Auto-reject**: Tasks rejected if deadline exceeded
- **PR validation**: GitHub PR required to approve
- **Review required**: Tech Lead review mandatory
- **Daily cron**: Automated deadline checks

### 4. Evaluation
- Sprint-based appraisals
- 4-point rating system (1-5 scale)
- Auto-calculated overall rating
- CEO evaluation interface

### 5. Documentation
- Structured folder system
- SRS, Design, Reports, Final folders
- Permission-based access

---

## Quick Reference

### First Time Setup
1. `docker-compose up -d` - Start services
2. Visit http://SERVER_IP:8069
3. Create database: `artemis_lab`
4. Install 5 modules (Employees, Project, Documents, Discuss, Appraisals)
5. Install `artemis_custom` module (custom features)
6. Create 9 user groups
7. Add interns as employees

→ See [SETUP_GUIDE.md](SETUP_GUIDE.md) for complete step-by-step

### Deployment Schedule
Day 1: Docker + Database  
Day 2: Modules  
Day 3: Users + Employees  
Day 4: Projects + Sprints  
Day 5: Automation rules  
Day 6: Roles & permissions  
Day 7: Testing + Launch  

→ See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for daily tasks

### Essential Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f odoo

# Run backup
./scripts/daily_backup.sh

# Restore backup
./scripts/restore_backup.sh backups/db_backup_*.sql.gz

# Health check
./scripts/health_check.sh

# Quarter reset (DELETE DATA!)
./scripts/quarter_reset.sh
```

---

## Custom Module (artemis_custom)

**All company-like features in one module:**

### Models Extended
- `hr.employee` → Added batch, skills, GitHub, role
- `project.project` → Added team members, GitHub repo, doc status
- `project.task` → Added reviewer, PR link, custom stages, deadline check

### New Models
- `artemis.evaluation` - Appraisal system with ratings
- `artemis.skill` - Skill catalog
- `artemis.document.folder` - Document structure

### Server Actions
- Auto-reject on deadline
- PR link validation
- Review requirement enforcement
- Cron job for daily checks

### User Groups
```
Intern           → Own task update
Developer         → Code-related tasks
Designer          → Design & 3D visualization tasks
AI Engineer    → AI & ML tasks
Tech Lead         → Review + approve
Project Manager   → Assign + plan
QA Tester         → Testing tasks
CEO               → Evaluate all
System Admin      → Everything
```

---

## Task Workflow

```
Todo
  ↓
In Progress
  ↓
In Review (Requires reviewer assignment)
  ↓
Approved (Requires GitHub PR link)
  ├─→ Success ✓
  └─→ Deadline exceeded? → REJECTED ✗
```

---

## Backup Strategy

### Daily Backup (Automatic)
- Runs at 2 AM via cron
- Compressed backup in `backups/`
- Keeps last 30 days only

### Manual Backup
```bash
docker exec artemis_postgres pg_dump -U odoo postgres > backups/manual_backup.sql
gzip backups/manual_backup.sql
```

### Restore from Backup
```bash
./scripts/restore_backup.sh backups/db_backup_*.sql.gz
```

### Quarter Reset (Destructive!)
```bash
./scripts/quarter_reset.sh
# Keeps: employees, users, modules, config
# Deletes: projects, tasks, evaluations
```

---

## System Requirements

- **OS**: Ubuntu 22.04 LTS
- **RAM**: 4 GB minimum (8 GB recommended)
- **CPU**: 2 cores
- **Storage**: 32 GB
- **Docker**: 20.10+
- **Docker Compose**: 1.29+

---

## Support & Troubleshooting

### Containers Won't Start
```bash
docker-compose logs odoo
# Check: Port in use? RAM? Disk space?
```

### Module Installation Error
```bash
docker exec artemis_odoo rm -rf /var/lib/odoo/addons
docker-compose restart odoo
# Reinstall from Apps
```

### Database Corrupted
```bash
./scripts/restore_backup.sh backups/latest_backup.sql.gz
```

### Automation Rules Not Working
- Settings → Automation → Server Actions
- Verify all 3 actions exist
- Check Cron configuration
- Review system logs

---

## Default Credentials

**After setup:**
- **Admin Email**: admin@artemis-lab.local
- **Admin Password**: [Set during DB creation]
- **Database**: artemis_lab
- **Postgres User**: odoo
- **Postgres Password**: odoo

**Store admin credentials securely!**

---

## Next Steps

1. **Read [SETUP_GUIDE.md](SETUP_GUIDE.md)** for complete walkthrough
2. **Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** for 7-day plan
3. **Make scripts executable**: `chmod +x scripts/*.sh`
4. **Start services**: `docker-compose up -d`
5. **Access Odoo**: http://SERVER_IP:8069

---

## Real Company Features ✓

This isn't a tutorial system - it's a **real operating system** for:

- ✅ **Employee portfolios** - Real company work experience
- ✅ **Professional deployments** - Professional setup
- ✅ **MoU compliance** - No renaming needed
- ✅ **Production deployment** - Backup, restore, automation
- ✅ **Industry standard** - Odoo ERP, GitHub integration, sprint planning

**Everything you need for a real R&D lab.**

---

**Version**: 1.0  
**Status**: Ready for Deployment  
**Maintenance**: By Artemis System Admin
