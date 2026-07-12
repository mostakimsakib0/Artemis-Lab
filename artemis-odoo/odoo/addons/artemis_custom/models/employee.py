from odoo import models, fields


class ArtemisEmployee(models.Model):
    _inherit = 'hr.employee'

    batch = fields.Selection(
        [('2024', 'Batch 2024'), ('2025', 'Batch 2025'), ('2026', 'Batch 2026')],
        string='Batch'
    )
    skills = fields.Many2many('artemis.skill', string='Skills')
    github_username = fields.Char('GitHub Username')
    role_tag = fields.Selection(
        [
            ('intern', 'Intern'),
            ('developer', 'Developer'),
            ('designer', 'Designer'),
            ('ai_engineer', 'AI Engineer'),
            ('tech_lead', 'Tech Lead'),
            ('project_manager', 'Project Manager'),
            ('qa_tester', 'QA Tester'),
            ('ceo', 'CEO'),
            ('system_admin', 'System Admin'),
        ],
        string='Role Tag'
    )
