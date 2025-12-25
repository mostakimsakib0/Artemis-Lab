# MIU Software R&D Lab

**A production-ready software company simulation platform built on Odoo 17 + Docker**

> This system transforms a university lab into a real software company where students work on actual projects with professional workflows.

---

## Quick Start (5 minutes)

```bash
# 1. Navigate to project
cd miu-odoo

# 2. Start services
docker-compose up -d

# 3. Wait 60 seconds, then open browser
# http://localhost:8069

# 4. Create database
# Database: miu_rnd_lab
# Email: admin@miu-rnd.lab
# Company: MIU Software R&D Lab
```

---

## What is This?

### ✅ Real Software Company Features

- **Students = Employees** with roles (Developer, QA, Student, etc.)
- **Projects & Sprints** with deadlines and milestones
- **Task Management** with GitHub PR integration
- **Evaluation System** for sprint-based appraisals
- **Automation Rules** for workflow discipline
- **Document Management** for SRS, design, reports
- **Role-Based Access Control** for 7 different roles

### ✅ Not a Tutorial Platform

- Professional naming conventions
- Real-world constraints (PR requirement, review mandatory, deadline enforcement)
- Backup & disaster recovery system
- Production-grade deployment
- MoU-ready documentation

---

## System Architecture

```
MIU Software R&D Lab
├── Frontend: Odoo Web Interface (Port 8069)
│   └── React-based UI
├── Backend: Odoo Community Edition 17.0
│   ├── Custom Module (miu_custom)
│   └── 5 Mandatory Modules
└── Database: PostgreSQL 14
    └── Persistent storage (postgres/data/)
```

### Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| **Odoo** | 17.0 Community | ERP framework |
| **PostgreSQL** | 14 | Database |
| **Docker** | 20.10+ | Containerization |
| **Python** | 3.11 | Backend |
| **React** | Latest | Frontend |

---

## Directory Structure

```
miu-odoo/
├── docker-compose.yml         # Core infrastructure
├── odoo/
│   ├── config/
│   │   └── odoo.conf         # Server configuration
│   ├── addons/
│   │   └── miu_custom/       # Custom module with all MIU features
│   │       ├── models/       # Business logic
│   │       ├── views/        # UI forms
│   │       ├── security/     # Access control
│   │       └── data/         # Initial data
│   └── data/                 # Runtime data
├── postgres/
│   └── data/                 # Database files
├── backups/                  # Daily backups
├── scripts/
│   ├── daily_backup.sh      # Automated backup
│   ├── restore_backup.sh    # Database recovery
│   ├── semester_reset.sh    # Clean slate for new batch
│   └── health_check.sh      # System health monitor
├── SETUP_GUIDE.md           # Complete setup guide
└── DEPLOYMENT_CHECKLIST.md  # Week-by-week checklist
```

---

## Installation

### Prerequisites

```bash
# Minimum system
OS: Ubuntu 22.04 LTS
RAM: 4 GB (8 GB recommended)
CPU: 2 cores
Storage: 32 GB

# Required software
Docker 20.10+
Docker Compose 1.29+
Git
```

### Setup Steps

#### Step 1: Install Docker

```bash
sudo apt update
sudo apt install docker.io docker-compose git -y
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

#### Step 2: Start Services

```bash
cd miu-odoo
docker-compose up -d
```

#### Step 3: Access Odoo

```
Browser: http://localhost:8069
Database: miu_rnd_lab
Email: admin@miu-rnd.lab
```

#### Step 4: Install Modules

In Odoo interface → **Apps** → Install these (in order):
1. Employees
2. Project
3. Documents
4. Discuss
5. Appraisals

#### Step 5: Activate Custom Module

**Apps** → Search `miu` → Install **MIU Custom Module**

---

## Usage

### For Project Manager

1. **Create Project**
   - Go to Project → Projects → Create
   - Set name, batch, GitHub repo
   - Add team members

2. **Create Sprints** (Milestones)
   - Go to Milestones
   - Create 3 sprints (Design, Development, Testing)

3. **Assign Tasks**
   - Create task with title, deadline, reviewer
   - Set milestone and assignee
   - Save (auto-validation enforced)

### For Students

1. **Update Task Status**
   - Go to My Tasks
   - Move between stages: Todo → In Progress → In Review
   - Add GitHub PR link when ready

2. **Get Reviewed**
   - Tech Lead reviews and approves
   - System validates PR link exists
   - Cannot approve without PR

### For Faculty

1. **Evaluate Students**
   - Go to HR → Evaluations
   - Create appraisal per sprint
   - Rate on 4 criteria (1-5 scale)
   - System calculates overall rating

---

## Key Features

### 🔒 Role-Based Access Control

| Role | Can View | Can Assign | Can Review | Can Evaluate |
|------|----------|-----------|-----------|-------------|
| **Student** | Own tasks | ❌ | ❌ | ❌ |
| **Developer** | Team tasks | ✓ | ❌ | ❌ |
| **Tech Lead** | All tasks | ✓ | ✓ | ❌ |
| **Project Manager** | All | ✓ | ❌ | ❌ |
| **Faculty** | Employee records | ❌ | ❌ | ✓ |
| **System Admin** | Everything | ✓ | ✓ | ✓ |

### ⚙️ Automation Rules

1. **Deadline Enforcement**
   - Task deadline exceeded → Auto-reject
   - Runs daily via cron job
   - Notification sent automatically

2. **PR Link Requirement**
   - Cannot move to "Approved" without GitHub PR
   - Validated before stage change
   - Enforces code discipline

3. **Review Mandatory**
   - Tech Lead must be assigned as reviewer
   - Review stage is mandatory before approval
   - System enforces workflow

### 📊 Evaluation System

- **One evaluation per student per sprint**
- **4 rating criteria**:
  - Task completion
  - Code discipline
  - Communication
  - Consistency
- **Auto-calculated overall rating**
- **Faculty-generated reports**

---

## Backup & Recovery

### Daily Automatic Backup

```bash
# Add to crontab (runs daily at 2 AM)
0 2 * * * docker exec miu_postgres pg_dump -U odoo postgres > /path/to/backups/db_$(date +\%Y\%m\%d).sql
```

### Manual Backup

```bash
./scripts/daily_backup.sh
```

### Restore from Backup

```bash
./scripts/restore_backup.sh backups/db_backup_YYYYMMDD.sql.gz
```

### Semester Reset (Keep History)

```bash
./scripts/semester_reset.sh
```

---

## Health Monitoring

### Check System Status

```bash
./scripts/health_check.sh
```

Returns:
- Docker containers running ✓
- PostgreSQL connectivity ✓
- Odoo port availability ✓
- Database size
- Disk usage
- Recent error count
- Latest backup time

### View Logs

```bash
# Odoo logs
docker logs -f miu_odoo

# PostgreSQL logs
docker logs -f miu_postgres
```

---

## Troubleshooting

### Docker Container Won't Start

```bash
# Check logs
docker-compose logs odoo

# Restart
docker-compose restart

# Full reset (keep data)
docker-compose down
docker-compose up -d
```

### Port 8069 Already in Use

```bash
# Find what's using it
lsof -i :8069

# Kill the process or change port in docker-compose.yml
# Change "8069:8069" to "8070:8069"
```

### Database Connection Error

```bash
# Verify PostgreSQL
docker exec miu_postgres psql -U odoo -c "SELECT 1"

# Reset connection
docker-compose restart db odoo
```

### Module Installation Error

```bash
# Clear Odoo cache
docker exec miu_odoo rm -rf /var/lib/odoo/addons

# Restart
docker-compose restart odoo
```

---

## Documentation

| Document | Purpose |
|----------|---------|
| [SETUP_GUIDE.md](miu-odoo/SETUP_GUIDE.md) | Complete configuration guide (100+ page equivalent) |
| [DEPLOYMENT_CHECKLIST.md](miu-odoo/DEPLOYMENT_CHECKLIST.md) | Week-by-week deployment checklist |
| [README.md](miu-odoo/README.md) | Quick reference |

---

## One-Week Rollout Plan

| Day | Task | Time |
|-----|------|------|
| **1** | Docker setup, containers running | 3 hrs |
| **2** | Odoo config, module installation | 4 hrs |
| **3** | User groups, faculty/PM setup | 3 hrs |
| **4** | Student employee records | 4 hrs |
| **5** | Project, sprints, sample tasks | 4 hrs |
| **6** | Permission testing, automation | 3 hrs |
| **7** | Training, documentation, go-live | 4 hrs |

**Total**: 25 hours (can be condensed to 3-4 days with parallel work)

---

## Performance Specifications

| Metric | Value |
|--------|-------|
| **Max Concurrent Users** | 50+ (with 4 GB RAM) |
| **Task Load** | 1000+ tasks per project |
| **Database Size** | Grows ~50-100 MB per 100 students per semester |
| **Backup Time** | ~2-5 minutes (depending on size) |
| **Restore Time** | ~3-10 minutes |

For larger deployments:
- Increase RAM to 8+ GB
- Increase workers in `odoo.conf`
- Use database connection pooling

---

## Important Notes

### ✅ DO

- Use GitHub PR links for all tasks
- Review before approval
- Maintain regular backups
- Document all processes
- Use milestones for sprints
- Enforce naming conventions

### ❌ DON'T

- Mix code & DB in one container
- Give students admin rights
- Skip PR discipline
- Change folder structure
- Install random apps
- Skip backup testing

---

## Support & Contact

- **Documentation**: See [SETUP_GUIDE.md](miu-odoo/SETUP_GUIDE.md)
- **Issues**: Check troubleshooting section above
- **Admin Email**: admin@miu-rnd.lab
- **Odoo Docs**: https://www.odoo.com/documentation/17.0/

---

## License

This project is configured for MIU Software R&D Lab.
Custom module and configuration are proprietary.

---

## Version Info

- **Odoo**: 17.0 Community
- **PostgreSQL**: 14
- **Docker**: 20.10+
- **Last Updated**: December 2025

---

**This is a production-ready system, not a tutorial.**
**It can be presented to universities and partners as a real software company simulation.**