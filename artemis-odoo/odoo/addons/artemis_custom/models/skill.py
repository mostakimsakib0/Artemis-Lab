from odoo import models, fields


class ArtemisSkill(models.Model):
    _name = 'artemis.skill'
    _description = 'Artemis Skill'

    name = fields.Char(string='Skill Name', required=True)
    category = fields.Selection(
        [('backend', 'Backend'), ('frontend', 'Frontend'), ('devops', 'DevOps'), ('qa', 'QA')],
        string='Category'
    )
