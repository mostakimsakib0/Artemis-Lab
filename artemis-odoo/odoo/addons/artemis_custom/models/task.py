from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class ArtemisTask(models.Model):
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
        for record in self:
            if record.date_deadline:
                record.deadline_exceeded = datetime.now().date() > record.date_deadline.date()
            else:
                record.deadline_exceeded = False

    @api.constrains('custom_stage', 'github_pr_link')
    def _check_pr_link_required(self):
        for record in self:
            if record.custom_stage == 'approved' and not record.github_pr_link:
                raise ValidationError('GitHub PR link is required to move to Approved status.')

    def action_reject_if_deadline_exceeded(self):
        for record in self:
            if record.deadline_exceeded and record.custom_stage != 'approved':
                record.custom_stage = 'rejected'

    def action_require_review(self):
        for record in self:
            if record.custom_stage == 'in_review' and not record.reviewer_id:
                raise ValidationError('Reviewer must be assigned before review can proceed.')
