# Artemis Lab - Deployment Checklist

> **Building Intelligent Software, AI & Design Solutions.**  
> Software Development · AI Solutions · R&D · Interior Design & 3D Visualization · Automation · Cloud & DevOps

Complete this checklist for a successful one-week rollout.

---

## Phase 1: Infrastructure Setup (Day 1)

### System Requirements ✓
- [ ] Ubuntu 22.04 LTS installed
- [ ] 4+ GB RAM available
- [ ] 2+ CPU cores
- [ ] 32+ GB storage
- [ ] Internet connection stable
- [ ] SSH access to server

### Team Preparation
- [ ] System admin trained on Docker
- [ ] CEO assigned
- [ ] Project manager identified
- [ ] 15-25 interns ready (with emails)

---

## WEEK 1: DAILY CHECKLIST

### **DAY 1: DOCKER SETUP (3 hours)**

**Morning (08:00-11:00)**

- [ ] Install Docker
  ```bash
  sudo apt update
  sudo apt install docker docker-compose git -y
  sudo systemctl enable docker
  ```

- [ ] Verify installations
  ```bash
  docker --version
  docker-compose --version
  ```

- [ ] Clone repository (or setup artemis-odoo folder)
  ```bash
  cd /path/to/workspace
  ls -la artemis-odoo/
  ```

- [ ] Check folder structure
  ```bash
  tree artemis-odoo/ -L 3
  ```
  Should match expected structure ✓

- [ ] Start Docker containers
  ```bash
  cd artemis-odoo
  docker-compose up -d
  ```

- [ ] Verify containers running
  ```bash
  docker ps
  # Should show artemis_odoo and artemis_postgres
  ```

- [ ] Check logs for errors
  ```bash
  docker-compose logs odoo | grep -i error
  ```

**Afternoon (14:00-17:00)**

- [ ] Access Odoo at http://SERVER_IP:8069
- [ ] See database creation screen
- [ ] Database name: `artemis_lab`
- [ ] Email: `admin@artemis-lab.local`
- [ ] Password: Set strong password (save in secure place!)
- [ ] Country: Bangladesh
- [ ] Language: English
- [ ] Company name: `Artemis Lab`
- [ ] Click **Create Database**
- [ ] System loads dashboard
- [ ] Admin login works
- [ ] Log out and verify login again

**Evening (After 17:00)**
- [ ] Document server IP and credentials
- [ ] Inform CEO about access
- [ ] Backup current state

---

### **DAY 2: MODULE INSTALLATION (3 hours)**

**Morning (09:00-12:00)**

- [ ] Login as admin
- [ ] Go to **Apps**
- [ ] Search and install: **Employees** (hr)
  - [ ] Wait for installation complete
  - [ ] Verify no errors
  - [ ] Check HR menu appears

- [ ] Search and install: **Project** (project)
  - [ ] Wait for installation complete
  - [ ] Verify no errors
  - [ ] Check Project menu appears

- [ ] Search and install: **Documents** (documents)
  - [ ] Verify installed
  - [ ] Check Documents menu appears

- [ ] Search and install: **Discuss** (mail)
  - [ ] Verify installed

- [ ] Search and install: **Appraisals** (hr_appraisal)
  - [ ] Verify installed

**Afternoon (14:00-17:00)**

- [ ] Install **artemis_custom** module
  - [ ] Enable Developer Mode
    - Go to Settings → Activate Developer Mode
  - [ ] Go to Apps → search "artemis"
  - [ ] Install **Artemis Custom Module**
  - [ ] Wait for installation (might take 2-3 minutes)
  - [ ] Check for error messages
  - [ ] Verify new menu items appear

- [ ] Verify module installations
  ```
  Apps → Installed Apps filter
  Should show all 6 modules
  ```

- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Refresh Odoo interface

---

### **DAY 3: USER GROUPS & EMPLOYEES (4 hours)**

**Morning (08:00-12:00)**

**Create User Groups**
- [ ] Settings → Users & Companies → Groups
- [ ] Create group: **Intern**
- [ ] Create group: **Developer**
- [ ] Create group: **Tech Lead**
- [ ] Create group: **Project Manager**
- [ ] Create group: **QA Tester**
- [ ] Create group: **CEO**
- [ ] Create group: **System Admin**

All 9 groups created ✓

**Afternoon (14:00-17:00)**

**Create CEO User**
- [ ] Settings → Users & Companies → Users → Create
- [ ] Email: `ceo@artemis-lab.local`
- [ ] Name: CEO Name
- [ ] Groups: CEO + Development
- [ ] Save

**Create Project Manager User**
- [ ] Create user
- [ ] Email: `pm@artemis-lab.local`
- [ ] Name: Project Manager Name
- [ ] Groups: Project Manager + Development
- [ ] Save

**Create Sample Interns (5 minimum)**
- [ ] HR → Employees → Create
  - [ ] Name: Intern 1 Name
  - [ ] Role Tag: Intern
  - [ ] Batch: 2025
  - [ ] GitHub: username
  - [ ] Skills: Select 2-3
  - [ ] Save

- [ ] Repeat for 4 more interns
- [ ] Create system user for each
- [ ] Assign batch, skills, roles

**End of Day:**
- [ ] 1 CEO user created & tested
- [ ] 1 PM user created
- [ ] 5 intern employees created
- [ ] All users can login

---

### **DAY 4: PROJECT & SPRINT SETUP (4 hours)**

**Morning (09:00-13:00)**

**Create Main Project**
- [ ] Project → Projects → Create
- [ ] Name: `Artemis Lab – Batch 2025`
- [ ] Alias: `artemis-lab-2025`
- [ ] Enable:
  - [ ] Task dependencies
  - [ ] Milestones
- [ ] GitHub repo URL (if available): `https://github.com/...`
- [ ] Add all 5+ interns as team members
- [ ] Save

**Create Milestones (Sprints)**
- [ ] Project → Milestones → Create

  **Sprint 1: Requirement & Design**
  - [ ] Name: Sprint 1: Requirement & Design
  - [ ] Start: Week 1 (e.g., 2025-01-20)
  - [ ] Deadline: Week 2 end (e.g., 2025-02-02)
  - [ ] Description: Requirements, architecture design
  - [ ] Save

  **Sprint 2: Core Development**
  - [ ] Name: Sprint 2: Core Development
  - [ ] Start: Week 3 (e.g., 2025-02-03)
  - [ ] Deadline: Week 6 end (e.g., 2025-02-23)
  - [ ] Description: Backend & frontend development
  - [ ] Save

  **Sprint 3: Testing & Deployment**
  - [ ] Name: Sprint 3: Testing & Deployment
  - [ ] Start: Week 7 (e.g., 2025-02-24)
  - [ ] Deadline: Week 8 end (e.g., 2025-03-02)
  - [ ] Description: QA testing, deployment
  - [ ] Save

**Afternoon (14:00-17:00)**

**Create Sample Tasks (15 minimum)**

For each task:
- [ ] Project → Tasks → Create
- [ ] Title: [Specific task]
- [ ] Description: [Requirements]
- [ ] Assignee: [Intern name]
- [ ] Reviewer: [CEO/Tech Lead]
- [ ] Deadline: [Sprint deadline or earlier]
- [ ] Milestone: [Sprint 1/2/3]
- [ ] Save

**Sample Tasks to Create:**
1. [ ] Design authentication module (Sprint 1)
2. [ ] Design database schema (Sprint 1)
3. [ ] Setup API structure (Sprint 2)
4. [ ] Implement user registration (Sprint 2)
5. [ ] Build dashboard (Sprint 2)
6. [ ] Write unit tests (Sprint 3)
7. [ ] Performance testing (Sprint 3)
8. [ ] Deployment documentation (Sprint 3)
... (7 more tasks across sprints)

**End of Day:**
- [ ] 1 project created
- [ ] 3 sprints created
- [ ] 15+ tasks created
- [ ] All tasks assigned

---

### **DAY 5: AUTOMATION & RULES VERIFICATION (3 hours)**

**Morning (10:00-13:00)**

**Verify Server Actions**
- [ ] Settings → Automation → Server Actions
- [ ] Should see:
  - [ ] Auto-Reject Task on Deadline
  - [ ] Validate PR Link for Approval
  - [ ] Enforce Review Before Closure

- [ ] Each action has description & code ✓

**Test Rule 1: Deadline Rejection**
- [ ] Create test task with deadline = TODAY
- [ ] Custom stage: In Progress
- [ ] Manually trigger cron or wait for scheduled run
- [ ] Task should move to Rejected
- [ ] Check task status changed ✓

**Test Rule 2: PR Link Validation**
- [ ] Try to move task to Approved WITHOUT PR link
- [ ] System should block with error message ✓
- [ ] Add GitHub PR link
- [ ] Now move to Approved should work ✓

**Test Rule 3: Review Required**
- [ ] Try to approve task without reviewer assigned
- [ ] System should block ✓
- [ ] Assign reviewer (Tech Lead)
- [ ] Now approve should work ✓

**Afternoon (14:00-16:00)**

**Setup Backup Script**
- [ ] Edit `scripts/daily_backup.sh`
  - [ ] Update paths if needed
  - [ ] Verify script is executable
  - [ ] Test manual backup:
    ```bash
    ./scripts/daily_backup.sh
    ```
  - [ ] Check backup created in `backups/` ✓

- [ ] Add to crontab
  ```bash
  crontab -e
  # Add: 0 2 * * * /path/to/artemis-odoo/scripts/daily_backup.sh
  ```
  - [ ] Verify cron entry added ✓

- [ ] Test restore script
  - [ ] Verify `restore_backup.sh` is executable
  - [ ] Dry-run (don't actually restore):
    ```bash
    ./scripts/restore_backup.sh backups/[latest].sql.gz
    # Cancel when prompted
    ```

**End of Day:**
- [ ] All 3 automation rules verified working
- [ ] Backup script tested
- [ ] Restore script tested
- [ ] Cron job scheduled

---

### **DAY 6: ROLES & PERMISSIONS (3 hours)**

**Morning (09:00-12:00)**

**Test Each Role**

Create test user for each group and verify:

**1. Intern User**
- [ ] Create user: `intern.test@artemis-lab.local`
- [ ] Add to group: Intern
- [ ] Login as this user
- [ ] Can they view tasks? ✓
- [ ] Can they edit own task? ✓
- [ ] Can they assign task? ✗ (shouldn't be able to)
- [ ] Logout

**2. Developer User**
- [ ] Create user: `dev.test@artemis-lab.local`
- [ ] Add to group: Developer
- [ ] Login as this user
- [ ] Can view tasks? ✓
- [ ] Can edit tasks? ✓
- [ ] Can create tasks? ✓
- [ ] Can delete? ✗
- [ ] Logout

**3. Tech Lead User**
- [ ] Create user: `lead.test@artemis-lab.local`
- [ ] Add to group: Tech Lead
- [ ] Can assign reviewer role? ✓
- [ ] Can approve/reject? ✓
- [ ] Logout

**4. Project Manager User**
- [ ] Login as PM (created on Day 3)
- [ ] Can create/assign tasks? ✓
- [ ] Can plan sprints? ✓
- [ ] Can delete? ✗
- [ ] Logout

**5. CEO User**
- [ ] Login as CEO (created on Day 3)
- [ ] Can create evaluations? ✓
- [ ] Can view all tasks? ✓
- [ ] Can edit evaluations? ✓
- [ ] Logout

**6. Admin User**
- [ ] Login as admin
- [ ] Full access to everything ✓
- [ ] Can access settings? ✓

**Afternoon (14:00-17:00)**

**Documentation Folder Setup**
- [ ] Documents → Create workspace
- [ ] Name: `Artemis Lab – Batch 2025`
- [ ] Create subfolders:
  - [ ] SRS
  - [ ] Design
  - [ ] Reports
  - [ ] Final
- [ ] Assign permissions (CEO can delete)

**Evaluation Template**
- [ ] Go to Evaluations menu (HR → Evaluations)
- [ ] Create sample evaluation:
  - [ ] Employee: Intern 1
  - [ ] Sprint: Sprint 1
  - [ ] Task Completion: 4
  - [ ] Code Discipline: 3
  - [ ] Communication: 4
  - [ ] Consistency: 4
  - [ ] Overall (auto-calculated): 3.75 ✓
- [ ] Save

**End of Day:**
- [ ] All 6 roles tested
- [ ] Permissions verified
- [ ] Documentation structure created
- [ ] Sample evaluation created

---

### **DAY 7: FINAL TESTING & LAUNCH (5 hours)**

**Morning (08:00-13:00)**

**System Stability Test**
- [ ] Run health check script
  ```bash
  ./scripts/health_check.sh
  ```
  All checks should be ✓

- [ ] Restart Docker services
  ```bash
  docker-compose restart
  ```
  - [ ] Both containers restart ✓
  - [ ] Access Odoo again ✓

- [ ] Check database integrity
  ```bash
  docker exec artemis_postgres psql -U odoo -c "SELECT COUNT(*) FROM project_task;"
  ```
  Should return task count ✓

**Performance Test**
- [ ] Create 10 more tasks
- [ ] Filter tasks by sprint
- [ ] Filter by assignee
- [ ] Pagination works smoothly ✓
- [ ] No lag/timeout ✓

**Communication Test**
- [ ] Create task with message
- [ ] Add comment
- [ ] Verify email notification (if enabled)

**Afternoon (14:00-18:00)**

**Final Documentation**
- [ ] Update SETUP_GUIDE.md with:
  - [ ] Actual server IP
  - [ ] Actual admin credentials (store securely)
  - [ ] CEO contact info
  - [ ] Support process

- [ ] Create login guide for interns
  - [ ] How to access Odoo
  - [ ] How to view assigned tasks
  - [ ] How to update task status
  - [ ] How to add PR link
  - [ ] How to comment on tasks

- [ ] Create guide for CEO
  - [ ] How to create evaluation
  - [ ] How to approve/reject tasks
  - [ ] How to view intern progress

**System Handover**
- [ ] Admin credentials shared securely
- [ ] CEO trained (30 min session)
- [ ] PM trained (30 min session)
- [ ] 2-3 interns tested access
- [ ] Support contact established

**Final Checks Before Launch**
- [ ] [ ] All modules installed
- [ ] [ ] No error messages in logs
- [ ] [ ] Backup running
- [ ] [ ] All users can login
- [ ] [ ] Tasks display correctly
- [ ] [ ] Automation rules working
- [ ] [ ] Database backed up

---

## LAUNCH STATUS

**Go/No-Go Decision Criteria:**

### ✅ GO - System Ready if:
- [ ] All 6 modules installed without errors
- [ ] All users can login
- [ ] All 3 automation rules verified
- [ ] Database backups working
- [ ] Performance acceptable
- [ ] CEO trained
- [ ] Documentation complete

### ⛔ NO-GO - System Not Ready if:
- [ ] Any module installation errors
- [ ] Login failing for any user
- [ ] Automation rules not working
- [ ] Backup failing
- [ ] Performance issues (timeout/lag)
- [ ] Critical data loss detected

---

## POST-LAUNCH (Week 2+)

**Weekly Tasks**
- [ ] Monitor daily backup logs
- [ ] Check system performance
- [ ] Review intern feedback
- [ ] Check for error logs
- [ ] Verify evaluation creation by CEO

**Monthly Tasks**
- [ ] Database maintenance (VACUUM)
- [ ] Review old backups, delete if > 30 days
- [ ] Update documentation if needed
- [ ] Performance tuning if needed

**Quarter End**
- [ ] Create full backup before reset
- [ ] Run quarter_reset.sh
- [ ] Create new project for next batch
- [ ] Archive old batch data

---

## TROUBLESHOOTING REFERENCE

| Issue | Solution |
|-------|----------|
| Containers won't start | `docker-compose logs odoo` check RAM/disk |
| Port 8069 in use | `lsof -i :8069` and kill process |
| Module won't install | Clear cache: `rm -rf /var/lib/odoo/*`, restart |
| Tasks not auto-rejecting | Check cron: `crontab -l` and settings |
| Can't login | Check user in Settings → Users, verify email |
| Database corrupted | Restore from backup: `./restore_backup.sh` |

---

## SUCCESS CRITERIA

**System is LIVE and operational when:**

1. ✅ 15+ interns successfully login
2. ✅ CEO can create & view evaluations
3. ✅ At least 15 tasks assigned
4. ✅ Automation rules proven working
5. ✅ Daily backup completed successfully
6. ✅ No critical errors in logs
7. ✅ All team trained and confident

---

## SUPPORT CONTACTS

- **System Admin Email**: [FILL IN]
- **CEO Lead Email**: [FILL IN]
- **Emergency Contact**: [FILL IN]
- **Artemis GitHub**: https://github.com/artemis-lab/

---

**Document Version**: 1.0  
**Last Updated**: December 25, 2024  
**Status**: Ready for Deployment
