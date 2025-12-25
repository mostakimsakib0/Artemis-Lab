# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class MIUEmployee(models.Model):
    """Extended Employee model with MIU-specific fields"""
    _inherit = 'hr.employee'

    batch = fields.Selection(
        [('2024', 'Batch 2024'), ('2025', 'Batch 2025'), ('2026', 'Batch 2026')],
        string='Batch'
    )
    skills = fields.Many2many('miu.skill', string='Skills')
    github_username = fields.Char('GitHub Username')
    role_tag = fields.Selection(
        [
            ('student', 'Student'),
            ('developer', 'Developer'),
            ('tech_lead', 'Tech Lead'),
            ('project_manager', 'Project Manager'),
            ('qa_tester', 'QA Tester'),
            ('faculty_mentor', 'Faculty Mentor'),
            ('system_admin', 'System Admin'),
        ],
        string='Role Tag'
    )


class MIUSkill(models.Model):
    """Skills catalog for employees"""
    _name = 'miu.skill'
    _description = 'MIU Skill'

    name = fields.Char(string='Skill Name', required=True)
    category = fields.Selection(
        [('backend', 'Backend'), ('frontend', 'Frontend'), ('devops', 'DevOps'), ('qa', 'QA')],
        string='Category'
    )


class MIUProject(models.Model):
    """Extended Project model"""
    _inherit = 'project.project'

    batch = fields.Char('Batch', default='2025')
    github_repo = fields.Char('GitHub Repository URL')
    documentation_status = fields.Selection(
        [('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
        string='Documentation Status'
    )
    team_members = fields.Many2many('hr.employee', string='Team Members')


class MIUTask(models.Model):
    """Extended Task model with company-like features"""
    _inherit = 'project.task'

    github_pr_link = fields.Char('GitHub PR Link')
    reviewer_id = fields.Many2one('hr.employee', string='Reviewer (Tech Lead)')
    custom_stage = fields.Selection(
        [
            ('todo', 'Todo'),
            ('in_progress', 'In Progress'),
            ('in_review', 'In Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Custom Stage',
        default='todo'
    )
    deadline_exceeded = fields.Boolean('Deadline Exceeded', compute='_compute_deadline_exceeded')

    @api.depends('date_deadline')
    def _compute_deadline_exceeded(self):
        """Check if deadline has passed"""
        for record in self:
            if record.date_deadline:
                record.deadline_exceeded = datetime.now().date() > record.date_deadline.date()
            else:
                record.deadline_exceeded = False

    @api.constrains('custom_stage', 'github_pr_link')
    def _check_pr_link_required(self):
        """Enforce PR link requirement for Approved stage"""
        for record in self:
            if record.custom_stage == 'approved' and not record.github_pr_link:
                raise ValidationError('GitHub PR link is required to move to Approved status.')

    def action_reject_if_deadline_exceeded(self):
        """Server action: Move to Rejected if deadline exceeded"""
        for record in self:
            if record.deadline_exceeded and record.custom_stage != 'approved':
                record.custom_stage = 'rejected'

    def action_require_review(self):
        """Ensure review is done before closing"""
        for record in self:
            if record.custom_stage == 'in_review' and not record.reviewer_id:
                raise ValidationError('Reviewer must be assigned before review can proceed.')


class MIUEvaluation(models.Model):
    """Appraisal/Evaluation model"""
    _name = 'miu.evaluation'
    _description = 'MIU Evaluation (Appraisal)'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    sprint_id = fields.Many2one('project.milestone', string='Sprint')
    project_id = fields.Many2one('project.project', string='Project')
    
    task_completion_rating = fields.Integer('Task Completion', default=0)
    code_discipline_rating = fields.Integer('Code Discipline', default=0)
    communication_rating = fields.Integer('Communication', default=0)
    consistency_rating = fields.Integer('Consistency', default=0)
    
    comments = fields.Text('Comments')
    evaluated_by = fields.Many2one('hr.employee', string='Evaluated By')
    evaluation_date = fields.Date('Evaluation Date', default=lambda self: fields.Date.context_today(self))
    
    overall_rating = fields.Float('Overall Rating', compute='_compute_overall_rating')

    @api.depends(
        'task_completion_rating',
        'code_discipline_rating',
        'communication_rating',
        'consistency_rating'
    )
    def _compute_overall_rating(self):
        """Calculate average rating"""
        for record in self:
            ratings = [
                record.task_completion_rating,
                record.code_discipline_rating,
                record.communication_rating,
                record.consistency_rating
            ]
            if any(ratings):
                record.overall_rating = sum(ratings) / len([r for r in ratings if r > 0])
            else:
                record.overall_rating = 0


class MIUDocumentFolder(models.Model):
    """Custom document folder structure"""
    _name = 'miu.document.folder'
    _description = 'MIU Document Folder'

    name = fields.Char(string='Folder Name', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    folder_type = fields.Selection(
        [('srs', 'SRS'), ('design', 'Design'), ('reports', 'Reports'), ('final', 'Final')],
        string='Folder Type'
    )
    parent_id = fields.Many2one('miu.document.folder', string='Parent Folder')
    description = fields.Text('Description')
