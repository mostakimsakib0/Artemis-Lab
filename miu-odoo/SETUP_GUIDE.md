# MIU Software R&D Lab - Odoo Setup & Deployment Guide

## Project Overview

This is a **real software company simulation** built on Odoo Community + Docker. It manages:
- **Students** as employees with roles
- **Projects & Sprints** with tasks and milestones
- **Evaluations** (appraisals) per sprint
- **Automation rules** for task workflow
- **PR-based task management**

---

## Prerequisites

### System Requirements
- **OS**: Ubuntu 22.04 LTS
- **RAM**: 4 GB minimum (8 GB recommended)
- **CPU**: 2 cores
- **Storage**: 32 GB
- **Docker**: 20.10+
- **Docker Compose**: 1.29+

### Initial Setup Commands

```bash
sudo apt update
sudo apt install docker docker-compose git curl -y
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker

# Verify installations
docker --version
docker-compose --version
```

---

## Folder Structure (DO NOT CHANGE)

```
miu-odoo/
├── docker-compose.yml          # Core Docker configuration
├── odoo/
│   ├── config/
│   │   └── odoo.conf           # Odoo server config
│   ├── addons/
│   │   └── miu_custom/         # Custom module (all MIU features)
│   │       ├── __manifest__.py
│   │       ├── __init__.py
│   │       ├── models/
│   │       │   ├── __init__.py (contains all models)
│   │       │   └── server_actions.xml
│   │       ├── views/
│   │       ├── security/
│   │       ├── data/
│   │       └── [... other files ...]
│   └── data/                   # Runtime data
├── postgres/
│   └── data/                   # Database files (auto-created)
└── backups/                    # Daily database backups
```

---

## 1. Docker Deployment

### Start Services

```bash
cd /path/to/miu-odoo
docker-compose up -d
```

Check logs:
```bash
docker-compose logs -f odoo
```

Stop services:
```bash
docker-compose down
```

### Verify Running Containers

```bash
docker ps
# Expected output:
# miu_odoo (running)
# miu_postgres (running)
```

---

## 2. Odoo First-Time Configuration

### Access Odoo
- URL: `http://SERVER_IP:8069`
- Browser: Chrome, Firefox, or Edge

### Database Creation

1. **Create Database Screen** appears automatically
   - Database name: `miu_rnd_lab`
   - Email: `admin@miu-rnd.lab`
   - Password: Use strong password
   - Country: Bangladesh
   - Language: English

2. **Company Name**: `MIU Software R&D Lab`

3. **First login**: Use admin email and password

---

## 3. Install Mandatory Odoo Modules

Navigate to **Apps** → Search and install:

1. **Employees** (`hr`) - For employee/student records
2. **Project** (`project`) - For projects, tasks, milestones
3. **Documents** (`documents`) - For SRS, design, reports
4. **Discuss** (`mail`) - For team communication
5. **Appraisals** (`hr_appraisal`) - For evaluations

**DO NOT install random apps.** Only these 5.

---

## 4. Activate Custom Module (miu_custom)

1. **Developer Mode**: Login as admin → bottom-right corner → Enable "Developer Mode"
2. **Go to Apps** → Search `miu`
3. **Install** `MIU Custom Module`
4. Wait for installation to complete

This module adds:
- Custom task fields (GitHub PR, Reviewer, Custom Stages)
- Evaluation model
- Employee extensions (Batch, Skills, Role tag)
- Server actions (auto-reject on deadline, PR validation)
- User groups

---

## 5. User & Role Configuration

### Create User Groups

**Settings** → **Users & Companies** → **Groups**

Create 7 groups:
1. **Student**
2. **Developer**
3. **Tech Lead**
4. **Project Manager**
5. **QA Tester**
6. **Faculty Mentor**
7. **System Admin**

### Permission Matrix

| Role | Own Task | Assign | Review | Evaluate | Admin |
|------|----------|--------|--------|----------|-------|
| Student | ✓ | | | | |
| Developer | ✓ | ✓ | | | |
| Tech Lead | ✓ | ✓ | ✓ | | |
| Project Manager | ✓ | ✓ | | | |
| QA Tester | ✓ | ✓ | | | |
| Faculty | | | | ✓ | |
| System Admin | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 6. Employee Setup (Students)

Each student = employee record

**HR** → **Employees** → **Create**

Fill:
- **Name**: Student name
- **Role Tag**: Select from dropdown (Student/Developer/etc.)
- **Batch**: 2024/2025/2026
- **GitHub Username**: student's GitHub handle
- **Skills**: Select multiple (Django, React, etc.)
- **User Link**: Create system user for login

Example:
```
Name: Ahmed Khan
Role: Developer
Batch: 2025
GitHub: ahmedkhan-dev
Skills: Django, PostgreSQL, Docker
```

---

## 7. Project Setup

**Project** → **Projects** → **Create**

### Main Project: Batch 2025

**Name**: `MIU Software R&D Lab – Batch 2025`

**Enable**:
- Task dependencies ✓
- Milestones ✓

**Settings**:
- GitHub Repo: `https://github.com/miu-rnd/batch-2025`
- Documentation Status: Not Started

**Add team members**: Select all batch 2025 students

---

## 8. Sprint Setup (Milestones)

**Project** → **Milestones** → **Create**

Create 3 sprints:

### Sprint 1: Requirement & Design
- **Date Range**: Week 1-2
- **Description**: Requirements gathering, architecture design

### Sprint 2: Core Development
- **Date Range**: Week 3-6
- **Description**: Backend & frontend development

### Sprint 3: Testing & Deployment
- **Date Range**: Week 7-8
- **Description**: QA testing, deployment preparation

---

## 9. Task Creation Template

**Project** → **Tasks** → **Create**

### Required Fields (MUST FILL)

- **Title**: Clear, action-oriented
- **Description**: Context, acceptance criteria
- **Assignee**: Select team member
- **Deadline**: Specific date (Sprint end date max)
- **Milestone**: Select Sprint 1/2/3
- **Reviewer**: Assign Tech Lead
- **GitHub PR Link**: Will be filled during development

### Task Workflow Stages

```
Todo → In Progress → In Review → Approved → Rejected (if deadline exceeded)
```

### Example Task

```
Title: Design User Authentication Module
Description:
- Implement OAuth2 for login
- JWT token handling
- Session management

Assignee: Ahmed Khan (Developer)
Reviewer: Farhan Ahmed (Tech Lead)
Milestone: Sprint 2: Core Development
Deadline: 2025-02-28
GitHub PR: (Will be filled later)
```

---

## 10. Automation Rules (Server Actions)

These run automatically - **NO manual configuration needed** (already in miu_custom).

### Rule 1: Auto-Reject on Deadline

**Trigger**: Daily at 00:00

**Action**: If task deadline passed AND status ≠ Approved → move to Rejected

**Code** (already in models/server_actions.xml):
```python
for task in records:
    if task.date_deadline and today > task.date_deadline.date():
        if task.custom_stage != 'approved':
            task.custom_stage = 'rejected'
            task.message_post(body='Auto-rejected due to deadline.')
```

### Rule 2: PR Link Required for Approval

**Trigger**: Before saving

**Action**: Block approval if GitHub PR link is empty

**Code** (in model constraints):
```python
@api.constrains('custom_stage', 'github_pr_link')
def _check_pr_link_required(self):
    if record.custom_stage == 'approved' and not record.github_pr_link:
        raise ValidationError('PR link required!')
```

### Rule 3: Review Mandatory

**Trigger**: Before moving to Approved

**Action**: Ensure Tech Lead reviewer is assigned

**Code** (in model):
```python
def action_require_review(self):
    if task.custom_stage == 'in_review' and not task.reviewer_id:
        raise ValidationError('Assign reviewer first!')
```

---

## 11. Documentation Structure

**Documents** → **Create Folder**

### Folder per Project:

```
MIU Software R&D Lab – Batch 2025/
├── SRS/
│   ├── Project Requirements Specification.pdf
│   └── Use Cases.docx
├── Design/
│   ├── System Architecture.ppt
│   ├── Database Schema.jpg
│   └── UI Mockups/
├── Reports/
│   ├── Progress Report - Week 1.pdf
│   ├── Progress Report - Week 2.pdf
│   └── Issues & Risks.docx
└── Final/
    ├── Final Presentation.ppt
    └── Source Code Link.txt
```

**Permission**: Faculty only can delete. Students: read + upload in own folder.

---

## 12. Evaluation (Appraisal) System

One evaluation per student per sprint.

**HR** → **Appraisals** → **Create** (or use custom Evaluation menu)

### Criteria (Each 1-5 scale)

1. **Task Completion**: Did they complete assigned tasks?
2. **Code Discipline**: Followed naming conventions, documentation, standards?
3. **Communication**: Participated in discussions, PR reviews?
4. **Consistency**: Regular commits, steady progress, deadline compliance?

### Faculty Role

1. Open evaluation form
2. Fill all 4 criteria (1-5 rating)
3. Add comments
4. Save (overall rating auto-calculates)
5. System generates report

### Report Generation

```
SPRINT 2 EVALUATION - AHMED KHAN
Task Completion: 5/5
Code Discipline: 4/5
Communication: 5/5
Consistency: 4/5
Overall: 4.5/5
Comments: Strong developer, needs better documentation.
```

---

## 13. Backup Strategy

### Daily Backup (Add to Cron)

```bash
# Open crontab
crontab -e

# Add this line (runs daily at 2 AM)
0 2 * * * docker exec miu_postgres pg_dump -U odoo postgres > /path/to/miu-odoo/backups/db_$(date +\%Y\%m\%d).sql
```

### Manual Full Backup

```bash
docker exec miu_postgres pg_dump -U odoo postgres > backups/db_backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore from Backup

```bash
# Stop Odoo
docker-compose down

# Restore database
docker exec -i miu_postgres psql -U odoo postgres < backups/db_backup_YYYYMMDD.sql

# Start Odoo
docker-compose up -d
```

### Semester Reset (Keep History)

```bash
# 1. Full backup before reset
docker exec miu_postgres pg_dump -U odoo postgres > backups/db_semester_end_$(date +%Y%m%d).sql

# 2. Delete records from this semester (keep code)
# - Delete tasks, projects, evaluations
# - Keep employee/user records
# - Keep GitHub history (external)

# 3. Create new project for next semester
```

---

## 14. Common Operations

### Add New Student

1. **Create HR Employee**:
   - Go to HR → Employees → Create
   - Fill name, batch, skills, role
   - Save

2. **Create System User**:
   - Settings → Users & Companies → Users → Create
   - Email: firstname.lastname@miu-rnd.lab
   - Name: Full name
   - Groups: Select Student + Development group
   - Save

3. **Assign to Project**:
   - Go to Project → Edit
   - Add to Team Members
   - Save

### Assign Task

1. Project → Tasks → Create/Edit
2. Fill all required fields
3. Set Reviewer (Tech Lead)
4. Deadline = Sprint end date
5. Save

### Check Task Status

1. Project → Tasks → View
2. Filter by Milestone (Sprint)
3. Check Custom Stage column
4. Auto-reject happens at deadline

### Generate Evaluation Report

1. HR → Appraisals (or custom Evaluations)
2. Filter by Sprint
3. Check Overall Rating
4. Download/Print report

---

## 15. Critical "DO NOTs"

### ❌ DON'T

- Mix code & DB in one container (we separate)
- Give students admin rights (use groups)
- Skip naming conventions (`FirstName_LastName`)
- Bypass PR discipline (PR link is mandatory)
- Install random apps (installs bloat)
- Change folder structure (causes deployment issues)
- Mix batches in one project (create separate projects)

### ✅ DO

- Use GitHub PR links
- Review before approval
- Maintain backups (daily)
- Document everything
- Use milestones for sprints
- Assign reviewers
- Set strict deadlines

---

## One-Week Rollout Checklist

### **Day 1: Setup**
- [ ] Docker & Docker Compose installed
- [ ] `docker-compose up -d` successful
- [ ] Odoo accessible at port 8069
- [ ] Database created (`miu_rnd_lab`)
- [ ] Admin user login successful

### **Day 2: Modules & Configuration**
- [ ] 5 mandatory modules installed
- [ ] miu_custom module installed
- [ ] 7 user groups created
- [ ] Faculty user created & logged in
- [ ] Project Manager user created

### **Day 3: Data Setup**
- [ ] 10-15 students added as employees
- [ ] All students have system users
- [ ] All students assigned skills
- [ ] All students assigned batches
- [ ] Main project created

### **Day 4: Sprints & Workflow**
- [ ] 3 milestones (sprints) created
- [ ] 15-20 sample tasks created
- [ ] Each task has reviewer assigned
- [ ] Deadline dates set
- [ ] GitHub PR links configured (example)

### **Day 5: Automation & Rules**
- [ ] Server actions verified in Odoo
- [ ] Daily cron job added for deadline check
- [ ] Test task rejection (set past deadline)
- [ ] Test PR link validation
- [ ] Test review requirement

### **Day 6: Roles & Permissions**
- [ ] Student group has limited access
- [ ] Tech Lead can review tasks
- [ ] Project Manager can assign tasks
- [ ] Faculty can create evaluations
- [ ] Admin has full access
- [ ] Test permissions for each role

### **Day 7: Training & Documentation**
- [ ] Faculty trained on system
- [ ] Students given access & passwords
- [ ] Documentation folder structure created
- [ ] First evaluation template created
- [ ] Backup strategy tested
- [ ] System live for pilot batch

---

## Troubleshooting

### Docker Container Won't Start

```bash
# Check logs
docker-compose logs odoo

# Common issues:
# 1. Port 8069 already in use
docker ps | grep 8069

# 2. Database connection failed
docker-compose down && docker-compose up -d

# 3. Insufficient disk space
df -h
```

### Module Installation Error

```bash
# Clear Odoo cache
docker exec miu_odoo rm -rf /var/lib/odoo/addons
docker-compose restart odoo

# Reinstall module from Apps
```

### Backup Failed

```bash
# Test postgres connection
docker exec miu_postgres psql -U odoo -c "SELECT 1"

# Manual backup
docker exec miu_postgres pg_dump -U odoo postgres > test.sql

# Check backup file
ls -lh backups/
```

### Task Not Auto-Rejecting

```bash
# Check server actions are active
# Go to Settings → Automation → Server Actions

# Manually trigger
# Go to Task → Action → Run Server Actions
```

---

## Performance Tips

1. **Increase RAM**: 4 GB → 8 GB for 50+ users
2. **Database Maintenance**: Monthly `VACUUM` on PostgreSQL
3. **Log Cleanup**: Monthly clear old logs in `/var/lib/odoo/`
4. **Worker Threads**: Set `workers=4` in odoo.conf for 50+ concurrent users

---

## Contact & Support

- **System Admin**: admin@miu-rnd.lab
- **MIU GitHub**: https://github.com/miu-rnd/
- **Odoo Documentation**: https://www.odoo.com/documentation/17.0/

---

**This setup is production-ready for university demonstration, MoU requirements, and student portfolios.**
