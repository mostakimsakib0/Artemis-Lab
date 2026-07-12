# Artemis Lab — System Architecture & Data Flow

> **Building Intelligent Software, AI & Design Solutions.**  
> Software Development · AI Solutions · R&D · Interior Design & 3D Visualization · Automation · Cloud & DevOps

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT BROWSERS (Interns, CEO)         │
│                    http://SERVER_IP:8069                         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Docker Network (artemis_network)                  │
│                                                                   │
│  ┌──────────────────────┐          ┌──────────────────────┐     │
│  │   Odoo Container     │          │ PostgreSQL Container │     │
│  │   (artemis_odoo)         │◄────────►│  (artemis_postgres)      │     │
│  │                      │  TCP 5432 │                      │     │
│  │ • Odoo 17.0          │          │ • Port 5432          │     │
│  │ • Port 8069          │          │ • Database: postgres │     │
│  │ • Workers: 2         │          │ • User: odoo         │     │
│  │ • Memory: 512MB      │          │ • Password: odoo     │     │
│  │                      │          │                      │     │
│  │ Modules:             │          │ Data Volume:         │     │
│  │ • base, web          │          │ ./postgres/data/     │     │
│  │ • hr (Employees)     │          │                      │     │
│  │ • project (Tasks)    │          │ Persistence:         │     │
│  │ • documents          │          │ Survives restarts ✓  │     │
│  │ • mail               │          │                      │     │
│  │ • hr_appraisal       │          └──────────────────────┘     │
│  │ • artemis_custom ✓       │                                        │
│  │   (our module)       │                                        │
│  │                      │                                        │
│  │ Volumes:             │                                        │
│  │ ./odoo/config/       │                                        │
│  │ ./odoo/addons/       │                                        │
│  │ ./odoo/data/         │                                        │
│  └──────────────────────┘                                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ File System
                             ▼
        ┌─────────────────────────────────────────┐
        │     Host System Files (artemis-odoo/)        │
        │                                          │
        │ • Backups: ./backups/                   │
        │ • Config: ./odoo/config/                │
        │ • Addons: ./odoo/addons/artemis_custom/    │
        │ • Scripts: ./scripts/                   │
        └─────────────────────────────────────────┘
```

---

## User Roles & Permissions

```
┌─────────────────────────────────────────────────────────────┐
│                    USER GROUPS & ROLES                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SYSTEM ADMIN  ──► Full Access ✓✓✓✓✓✓✓✓✓✓                 │
│                   Everything                                │
│                                                              │
│  CEO       ──► View All, Evaluate ✓✓✓✓✓                │
│  MENTOR            • Create evaluations                     │
│                    • View intern progress                  │
│                    • Rate performance                       │
│                    • Generate reports                       │
│                                                              │
│  PROJECT       ──► Assign, Plan ✓✓✓✓                       │
│  MANAGER            • Create projects                       │
│                    • Create/assign tasks                    │
│                    • Set deadlines                          │
│                    • Manage sprints                         │
│                                                              │
│  TECH LEAD     ──► Review, Approve ✓✓✓✓                    │
│                    • Review code PRs                        │
│                    • Approve tasks                          │
│                    • Assign reviewers                       │
│                                                              │
│  DEVELOPER     ──► Code Tasks ✓✓✓                          │
│                    • Work on assigned tasks                 │
│                    • Submit PR links                        │
│                    • Update task status                     │
│                                                              │
│  QA TESTER     ──► Test Tasks ✓✓✓                          │
│                    • Testing assignment                     │
│                    • Bug reporting                          │
│                    • Task review                            │
│                                                              │
│  STUDENT       ──► Own Tasks ✓                             │
│                    • View assignments                       │
│                    • Update own tasks                       │
│                    • Submit work                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Models & Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    Artemis CUSTOM MODULE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  HR MODULE (Extended)                                       │
│  ┌──────────────┐                                           │
│  │  Employee    │                                           │
│  ├──────────────┤  1 ◄──────► * ┌──────────┐              │
│  │ name         │                │  Skill   │              │
│  │ batch ✓      │                ├──────────┤              │
│  │ skills ✓     │                │ name     │              │
│  │ github ✓     │                │ category │              │
│  │ role_tag ✓   │                └──────────┘              │
│  │ user_link    │                                           │
│  └──────────────┘                                           │
│         ▲                                                    │
│         │ 1                                                 │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐                                           │
│  │  Evaluation  │                                           │
│  ├──────────────┤                                           │
│  │ employee_id  │                                           │
│  │ sprint_id    │ ────► Project Milestone                  │
│  │ rating_1: 1-5│                                           │
│  │ rating_2: 1-5│                                           │
│  │ rating_3: 1-5│                                           │
│  │ rating_4: 1-5│                                           │
│  │ overall ✓    │ (auto-calculated)                        │
│  │ comments     │                                           │
│  └──────────────┘                                           │
│                                                              │
│                                                              │
│  PROJECT MODULE (Extended)                                  │
│  ┌──────────────┐        1       * ┌──────────────┐        │
│  │  Project     │◄──────────────────│  Task (Ext)  │        │
│  ├──────────────┤                   ├──────────────┤        │
│  │ name         │                   │ title        │        │
│  │ batch ✓      │                   │ description  │        │
│  │ github ✓     │                   │ assignee     │        │
│  │ doc_status ✓ │                   │ deadline     │        │
│  │ team ✓       │ (many-to-many)    │ milestone    │        │
│  └──────────────┘                   │ reviewer ✓   │        │
│         │                           │ pr_link ✓    │        │
│         │                           │ stage_custom │        │
│         │ 1                         │ deadline_exc │        │
│         ▼ *                         └──────────────┘        │
│  ┌──────────────┐                          ▲               │
│  │  Milestone   │                          │               │
│  │  (Sprint)    │                          │ many          │
│  ├──────────────┤                          │               │
│  │ name         │                  ┌───────┴─────────┐     │
│  │ start_date   │                  │ Task Dependency │     │
│  │ deadline     │                  └─────────────────┘     │
│  └──────────────┘                                           │
│                                                              │
│                                                              │
│  DOCUMENT MODULE (Custom)                                   │
│  ┌──────────────┐                                           │
│  │  Doc Folder  │                                           │
│  ├──────────────┤                                           │
│  │ name         │                                           │
│  │ project_id   │ ─────► Project                           │
│  │ folder_type  │        (SRS|Design|Reports|Final)        │
│  │ parent_id    │        (Hierarchical)                     │
│  │ description  │                                           │
│  └──────────────┘                                           │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Task Workflow & Automation

```
┌─────────────────────────────────────────────────────────────┐
│                  TASK LIFECYCLE WITH AUTOMATION              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  START                                                      │
│    │                                                        │
│    ▼                                                        │
│  ┌──────────┐                                              │
│  │  TODO    │  (Task created, unstarted)                   │
│  └─────┬────┘                                              │
│        │                                                    │
│        ▼                                                    │
│  ┌──────────────┐                                          │
│  │IN PROGRESS   │  (Work started)                          │
│  └─────┬────────┘                                          │
│        │                                                    │
│        ▼                                                    │
│  ┌──────────────┐                                          │
│  │ IN REVIEW    │  (Ready for review)                      │
│  │ [Auto-check] │  ✓ Reviewer assigned?                    │
│  └─────┬────────┘  ✗ Block if not                          │
│        │                                                    │
│        ▼                                                    │
│  ┌──────────────┐                                          │
│  │ APPROVED     │  (Tech Lead approved)                    │
│  │ [Auto-check] │  ✓ GitHub PR link exists?               │
│  │ [Auto-check] │  ✓ Deadline not exceeded?               │
│  └─────┬────────┘  ✗ Block if not                          │
│        │                                                    │
│        ├─ SUCCESS ──────────────┐                          │
│        │                        ▼                          │
│        │                    ┌────────┐                     │
│        │                    │ CLOSED │                     │
│        │                    └────────┘                     │
│        │                                                    │
│        ▼                                                    │
│  ┌──────────────┐          DAILY CRON JOB                  │
│  │ REJECTED ◄───┼──────── Checks deadline                  │
│  │ (Deadline    │         If exceeded & not approved      │
│  │  exceeded)   │         → REJECTED (auto)               │
│  └──────────────┘                                          │
│                                                              │
│                                                              │
│  AUTOMATION RULES:                                          │
│  ────────────────────────────────────────────────────────   │
│  Rule 1: Auto-Reject on Deadline                           │
│    Trigger: Daily cron @ 00:00                            │
│    Condition: deadline < today AND stage ≠ approved        │
│    Action: Move to rejected, send notification             │
│                                                              │
│  Rule 2: PR Link Required                                  │
│    Trigger: Before moving to approved                      │
│    Condition: github_pr_link is empty                      │
│    Action: Block transition, show error                    │
│                                                              │
│  Rule 3: Review Required                                   │
│    Trigger: Before moving to in_review/approved            │
│    Condition: reviewer_id is not set                       │
│    Action: Block transition, show error                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  SERVER DEPLOYMENT (Day 1-7)                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  DAY 1: Docker Setup                                        │
│  └─ Install Docker & Docker Compose                         │
│     └─ docker-compose up -d                                │
│        ├─ Start artemis_postgres (PostgreSQL 14)              │
│        └─ Start artemis_odoo (Odoo 17)                        │
│                                                               │
│  DAY 2: Module Installation                                │
│  └─ Install 5 mandatory modules                            │
│     ├─ HR (Employees)                                      │
│     ├─ Project (Tasks & Milestones)                       │
│     ├─ Documents                                           │
│     ├─ Mail (Discuss)                                      │
│     ├─ Appraisals                                          │
│     └─ Artemis Custom Module ✓ (all features)                 │
│                                                               │
│  DAY 3: User Configuration                                 │
│  └─ Create 9 user groups                                   │
│     ├─ Intern, Developer, Designer                       │
│     ├─ AI Engineer, Tech Lead                          │
│     ├─ Project Manager, QA Tester                         │
│     ├─ CEO, System Admin                                  │
│     └─ Create CEO & PM users                          │
│                                                               │
│  DAY 4: Project & Sprint Setup                             │
│  └─ Create Project: "Artemis Lab – Batch 2025"  │
│     ├─ Sprint 1: Requirement & Design (Week 1-2)         │
│     ├─ Sprint 2: Core Development (Week 3-6)             │
│     ├─ Sprint 3: Testing & Deployment (Week 7-8)         │
│     └─ Create 15+ sample tasks                            │
│                                                               │
│  DAY 5: Automation Verification                            │
│  └─ Verify server actions working                          │
│     ├─ Auto-reject on deadline ✓                         │
│     ├─ PR validation ✓                                    │
│     ├─ Review requirement ✓                               │
│     └─ Setup daily backup cron                            │
│                                                               │
│  DAY 6: Roles & Permissions Test                           │
│  └─ Test each role (Intern, Developer, etc.)            │
│     ├─ Verify permissions correct                         │
│     ├─ Create documentation structure                     │
│     └─ Create sample evaluation                           │
│                                                               │
│  DAY 7: Launch                                             │
│  └─ Final stability tests                                  │
│     ├─ Backup working ✓                                  │
│     ├─ Restore tested ✓                                  │
│     ├─ All modules functional ✓                          │
│     ├─ CEO & interns trained                         │
│     └─ System LIVE ✓                                     │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Data Persistence & Backup

```
┌────────────────────────────────────────────────────────┐
│          BACKUP & DATA PERSISTENCE STRATEGY             │
├────────────────────────────────────────────────────────┤
│                                                         │
│  DAILY AUTOMATED BACKUP                                │
│  ┌─────────────────────────────────────────┐          │
│  │  Cron Job (2 AM daily)                  │          │
│  │  ./scripts/daily_backup.sh              │          │
│  │  ├─ pg_dump postgres → .sql            │          │
│  │  ├─ gzip compression                   │          │
│  │  └─ Store in ./backups/                │          │
│  │      db_backup_YYYYMMDD_HHMMSS.sql.gz  │          │
│  │                                         │          │
│  │  Retention: 30 days (auto-delete old)   │          │
│  └─────────────────────────────────────────┘          │
│            │                                           │
│            ▼                                           │
│  STORAGE HIERARCHY                                    │
│  ┌─────────────────────────────────────────┐          │
│  │  Host File System: ./backups/           │          │
│  │  ├─ Daily backup files (compressed)    │          │
│  │  ├─ Quarter-end full backup           │          │
│  │  ├─ Manual backup (on-demand)          │          │
│  │  └─ Recovery tested & verified ✓       │          │
│  └─────────────────────────────────────────┘          │
│            │                                           │
│            ▼                                           │
│  RESTORE CAPABILITY                                   │
│  ┌─────────────────────────────────────────┐          │
│  │  ./scripts/restore_backup.sh <file>    │          │
│  │  ├─ Stop Odoo (keep postgres)           │          │
│  │  ├─ Decompress if .gz                  │          │
│  │  ├─ psql < backup.sql                  │          │
│  │  └─ Restart all services               │          │
│  │  ⏱ Recovery time: ~5 minutes           │          │
│  └─────────────────────────────────────────┘          │
│                                                         │
│                                                         │
│  SEMESTER RESET                                        │
│  ┌─────────────────────────────────────────┐          │
│  │  ./scripts/quarter_reset.sh            │          │
│  │  ├─ Full backup before reset            │          │
│  │  ├─ Delete projects & tasks             │          │
│  │  ├─ Delete evaluations                  │          │
│  │  ├─ Keep employees & users              │          │
│  │  ├─ Keep modules & config               │          │
│  │  └─ Ready for new batch                 │          │
│  └─────────────────────────────────────────┘          │
│                                                         │
│  VOLUME PERSISTENCE                                    │
│  ┌─────────────────────────────────────────┐          │
│  │  Docker Volumes (survive restarts):    │          │
│  │  ├─ ./postgres/data/ → DB files        │          │
│  │  ├─ ./odoo/config/ → Configuration     │          │
│  │  ├─ ./odoo/addons/ → Modules           │          │
│  │  └─ ./odoo/data/ → Runtime data        │          │
│  └─────────────────────────────────────────┘          │
│                                                         │
└────────────────────────────────────────────────────────┘
```

---

## Module Components

```
┌──────────────────────────────────────────────────────┐
│           Artemis CUSTOM MODULE STRUCTURE                 │
├──────────────────────────────────────────────────────┤
│                                                       │
│  __manifest__.py                                    │
│  └─ Module definition, dependencies, data files     │
│                                                       │
│  models/__init__.py (280+ lines)                   │
│  ├─ ArtemisEmployee (extended)                         │
│  │  • Batch field                                   │
│  │  • Skills many-to-many                          │
│  │  • GitHub username                              │
│  │  • Role tag                                      │
│  │                                                   │
│  ├─ ArtemisSkill                                        │
│  │  • Skill name                                   │
│  │  • Skill category                               │
│  │                                                   │
│  ├─ ArtemisProject (extended)                          │
│  │  • Batch designation                            │
│  │  • GitHub repo URL                              │
│  │  • Documentation status                         │
│  │  • Team members                                 │
│  │                                                   │
│  ├─ ArtemisTask (extended)                             │
│  │  • GitHub PR link                               │
│  │  • Reviewer assignment                          │
│  │  • Custom stages (5)                            │
│  │  • Deadline exceeded (computed)                 │
│  │  • Constraints & automations                    │
│  │                                                   │
│  ├─ ArtemisEvaluation (new)                            │
│  │  • Employee + sprint                            │
│  │  • 4 rating criteria (1-5 each)                │
│  │  • Overall rating (auto-calculated)             │
│  │  • Comments & evaluator                         │
│  │                                                   │
│  └─ ArtemisDocumentFolder (new)                        │
│     • Hierarchical folders                         │
│     • Project-linked                               │
│     • 4 folder types                               │
│                                                       │
│  views/ (4 XML files)                              │
│  ├─ artemis_employee_views.xml                         │
│  │  └─ Employee form with batch, skills, GitHub    │
│  │                                                   │
│  ├─ artemis_project_views.xml                          │
│  │  └─ Project form with repo, status, team        │
│  │                                                   │
│  ├─ artemis_task_views.xml                             │
│  │  └─ Task form with reviewer, PR, stages         │
│  │                                                   │
│  └─ artemis_evaluation_views.xml                       │
│     ├─ Evaluation form (4 ratings)                │
│     ├─ Evaluation list/tree view                  │
│     ├─ Action menu                                │
│     └─ HR menu integration                        │
│                                                       │
│  data/ (2 XML files)                               │
│  ├─ task_stages.xml                               │
│  │  └─ 5 task stages (Todo, In Progress, etc.)    │
│  │                                                   │
│  └─ user_groups.xml                               │
│     └─ 9 user groups                              │
│                                                       │
│  security/ (1 CSV file)                            │
│  └─ ir.model.access.csv                           │
│     ├─ Model-level permissions                    │
│     ├─ Group-based access control                 │
│     └─ Read/Write/Create/Delete rules             │
│                                                       │
│  models/server_actions.xml                         │
│  ├─ Server Action 1: Auto-reject on deadline      │
│  ├─ Server Action 2: PR link validation           │
│  ├─ Server Action 3: Review requirement           │
│  └─ Cron Job: Daily deadline check                │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

## Success Criteria

```
┌──────────────────────────────────────────────────────┐
│        SYSTEM LAUNCH SUCCESS CHECKLIST                │
├──────────────────────────────────────────────────────┤
│                                                       │
│  Infrastructure ✓                                   │
│  ├─ Docker containers running                      │
│  ├─ Database persistent across restarts            │
│  ├─ Port 8069 accessible                           │
│  └─ Logs clean (no critical errors)                │
│                                                       │
│  Modules ✓                                          │
│  ├─ 5 mandatory modules installed                  │
│  ├─ artemis_custom module fully functional             │
│  ├─ All menus & views visible                      │
│  └─ No module conflicts                            │
│                                                       │
│  Users ✓                                            │
│  ├─ 15+ interns successfully created              │
│  ├─ All users can login                            │
│  ├─ 9 groups assigned properly                     │
│  ├─ Permissions working correctly                  │
│  └─ No access issues                               │
│                                                       │
│  Automation ✓                                       │
│  ├─ Auto-reject on deadline working               │
│  ├─ PR link validation enforced                    │
│  ├─ Review requirement working                     │
│  └─ Cron job configured                            │
│                                                       │
│  Backup ✓                                           │
│  ├─ Daily backup completed                         │
│  ├─ Restore tested successfully                    │
│  ├─ Backup file compressed                         │
│  └─ Retention policy active                        │
│                                                       │
│  Testing ✓                                          │
│  ├─ 15+ tasks created & assigned                   │
│  ├─ Task workflow verified                         │
│  ├─ Evaluation system working                      │
│  ├─ No performance issues                          │
│  └─ No data loss detected                          │
│                                                       │
│  Training ✓                                         │
│  ├─ CEO trained (30 min)                       │
│  ├─ PM trained (30 min)                            │
│  ├─ Sample interns tested access                  │
│  ├─ Documentation provided                         │
│  └─ Support contact established                    │
│                                                       │
│  🎯 LAUNCH APPROVED - SYSTEM READY                 │
│                                                       │
└──────────────────────────────────────────────────────┘
```

---

**System Architecture Complete ✓**  
**All components integrated and documented**
