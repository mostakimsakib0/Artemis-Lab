from odoo import models, fields, api


class ArtemisEvaluation(models.Model):
    _name = 'artemis.evaluation'
    _description = 'Artemis Evaluation (Appraisal)'

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
        for record in self:
            ratings = [
                record.task_completion_rating,
                record.code_discipline_rating,
                record.communication_rating,
                record.consistency_rating
            ]
            non_zero = [r for r in ratings if r > 0]
            record.overall_rating = sum(ratings) / len(non_zero) if non_zero else 0
