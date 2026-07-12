from odoo import models, fields


class ArtemisProject(models.Model):
    _inherit = 'project.project'

    batch = fields.Char('Batch', default='2025')
    github_repo = fields.Char('GitHub Repository URL')
    documentation_status = fields.Selection(
        [('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')],
        string='Documentation Status'
    )
    team_members = fields.Many2many('hr.employee', string='Team Members')
