# MIU Software R&D Lab - Odoo Setup

**Complete production-ready setup for real software company simulation**

---

## Quick Start (2 minutes)

```bash
cd miu-odoo
docker-compose up -d
# Wait 30 seconds for services to start
# Visit: http://localhost:8069
```

---

## What's Included

✅ **Docker Setup** - Odoo 17 + PostgreSQL 14  
✅ **Custom Module** - Projects, tasks, evaluations, automation  
✅ **User Roles** - 7 group types (Student, Developer, Tech Lead, etc.)  
✅ **Automation** - Deadline rejection, PR validation, review requirement  
✅ **Backup Scripts** - Daily backup, restore, semester reset  
✅ **Complete Documentation** - Setup guide + deployment checklist  

---

## Folder Structure

```
miu-odoo/
├── docker-compose.yml          # Docker services config
├── SETUP_GUIDE.md              # 15-step complete guide
├── DEPLOYMENT_CHECKLIST.md     # 7-day deployment plan
├── odoo/
│   ├── config/odoo.conf        # Odoo server config
│   ├── addons/miu_custom/      # Custom module (all features)
│   └── data/                   # Runtime data
├── postgres/data/              # Database (auto-created)
├── backups/                    # Backups folder
└── scripts/
    ├── daily_backup.sh         # Auto-backup
    ├── restore_backup.sh       # Restore from backup
    ├── semester_reset.sh       # Reset data for next batch
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
- Student/Faculty/Admin profiles
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
- Faculty evaluation interface

### 5. Documentation
- Structured folder system
- SRS, Design, Reports, Final folders
- Permission-based access

---

## Quick Reference

### First Time Setup
1. `docker-compose up -d` - Start services
2. Visit http://SERVER_IP:8069
3. Create database: `miu_rnd_lab`
4. Install 5 modules (Employees, Project, Documents, Discuss, Appraisals)
5. Install `miu_custom` module (custom features)
6. Create 7 user groups
7. Add students as employees

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

# Semester reset (DELETE DATA!)
./scripts/semester_reset.sh
```

---

## Custom Module (miu_custom)

**All company-like features in one module:**

### Models Extended
- `hr.employee` → Added batch, skills, GitHub, role
- `project.project` → Added team members, GitHub repo, doc status
- `project.task` → Added reviewer, PR link, custom stages, deadline check

### New Models
- `miu.evaluation` - Appraisal system with ratings
- `miu.skill` - Skill catalog
- `miu.document.folder` - Document structure

### Server Actions
- Auto-reject on deadline
- PR link validation
- Review requirement enforcement
- Cron job for daily checks

### User Groups
```
Student           → Own task update
Developer         → Code-related tasks
Tech Lead         → Review + approve
Project Manager   → Assign + plan
QA Tester         → Testing tasks
Faculty Mentor    → Evaluate all
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
docker exec miu_postgres pg_dump -U odoo postgres > backups/manual_backup.sql
gzip backups/manual_backup.sql
```

### Restore from Backup
```bash
./scripts/restore_backup.sh backups/db_backup_*.sql.gz
```

### Semester Reset (Destructive!)
```bash
./scripts/semester_reset.sh
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
docker exec miu_odoo rm -rf /var/lib/odoo/addons
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
- **Admin Email**: admin@miu-rnd.lab
- **Admin Password**: [Set during DB creation]
- **Database**: miu_rnd_lab
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

- ✅ **Student portfolios** - Real company work experience
- ✅ **University demonstrations** - Professional setup
- ✅ **MoU compliance** - No renaming needed
- ✅ **Production deployment** - Backup, restore, automation
- ✅ **Industry standard** - Odoo ERP, GitHub integration, sprint planning

**Everything you need for a real R&D lab.**

---

**Version**: 1.0  
**Status**: Ready for Deployment  
**Maintenance**: By MIU System Admin
