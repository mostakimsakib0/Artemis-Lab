from odoo import models, fields, api
from datetime import datetime


class ArtemisDashboard(models.TransientModel):
    _name = 'artemis.dashboard'
    _description = 'CEO Dashboard'
    _rec_name = 'name'

    name = fields.Char(default='CEO Dashboard')

    # Projects
    total_projects = fields.Integer(compute='_compute_stats')
    active_projects = fields.Integer(compute='_compute_stats')

    # Tasks
    total_tasks = fields.Integer(compute='_compute_stats')
    tasks_todo = fields.Integer(compute='_compute_stats')
    tasks_in_progress = fields.Integer(compute='_compute_stats')
    tasks_in_review = fields.Integer(compute='_compute_stats')
    tasks_approved = fields.Integer(compute='_compute_stats')
    tasks_rejected = fields.Integer(compute='_compute_stats')
    overdue_tasks = fields.Integer(compute='_compute_stats')
    on_time_rate = fields.Float(compute='_compute_stats')

    # Evaluations
    total_evaluations = fields.Integer(compute='_compute_stats')
    avg_overall = fields.Float(compute='_compute_stats')
    avg_task_rating = fields.Float(compute='_compute_stats')
    avg_code_rating = fields.Float(compute='_compute_stats')
    avg_comm_rating = fields.Float(compute='_compute_stats')
    avg_consistency_rating = fields.Float(compute='_compute_stats')

    # Employees
    total_employees = fields.Integer(compute='_compute_stats')

    def _compute_stats(self):
        Task = self.env['project.task']
        Project = self.env['project.project']
        Evaluation = self.env['artemis.evaluation']
        Employee = self.env['hr.employee']

        today = datetime.now().date()

        for record in self:
            all_tasks = Task.search([])
            overdue = Task.search([
                ('date_deadline', '!=', False),
                ('date_deadline', '<', today),
                ('custom_stage', 'not in', ['approved', 'rejected'])
            ])
            completed = Task.search([('custom_stage', '=', 'approved')])
            total = len(all_tasks)

            record.total_projects = len(Project.search([]))
            record.active_projects = len(Project.search([('active', '=', True)]))
            record.total_tasks = total
            record.tasks_todo = len(Task.search([('custom_stage', '=', 'todo')]))
            record.tasks_in_progress = len(Task.search([('custom_stage', '=', 'in_progress')]))
            record.tasks_in_review = len(Task.search([('custom_stage', '=', 'in_review')]))
            record.tasks_approved = len(completed)
            record.tasks_rejected = len(Task.search([('custom_stage', '=', 'rejected')]))
            record.overdue_tasks = len(overdue)
            record.on_time_rate = round((len(completed) / total * 100) if total > 0 else 0, 1)

            evals = Evaluation.search([])
            record.total_evaluations = len(evals)
            if evals:
                record.avg_overall = round(sum(e.overall_rating for e in evals) / len(evals), 2)
                record.avg_task_rating = round(sum(e.task_completion_rating for e in evals) / len(evals), 1)
                record.avg_code_rating = round(sum(e.code_discipline_rating for e in evals) / len(evals), 1)
                record.avg_comm_rating = round(sum(e.communication_rating for e in evals) / len(evals), 1)
                record.avg_consistency_rating = round(sum(e.consistency_rating for e in evals) / len(evals), 1)
            else:
                record.avg_overall = 0
                record.avg_task_rating = 0
                record.avg_code_rating = 0
                record.avg_comm_rating = 0
                record.avg_consistency_rating = 0

            record.total_employees = len(Employee.search([]))

    def action_refresh(self):
        self._compute_stats()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'artemis.dashboard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'main',
        }


class ArtemisEmployeeDashboard(models.TransientModel):
    _name = 'artemis.employee.dashboard'
    _description = 'Employee Dashboard'

    name = fields.Char(compute='_compute_name')

    employee_id = fields.Many2one('hr.employee', string='Employee')

    # Tasks
    my_total_tasks = fields.Integer(compute='_compute_my_stats')
    my_todo = fields.Integer(compute='_compute_my_stats')
    my_in_progress = fields.Integer(compute='_compute_my_stats')
    my_in_review = fields.Integer(compute='_compute_my_stats')
    my_approved = fields.Integer(compute='_compute_my_stats')
    my_rejected = fields.Integer(compute='_compute_my_stats')
    my_overdue = fields.Integer(compute='_compute_my_stats')

    # Evaluations
    my_total_evaluations = fields.Integer(compute='_compute_my_stats')
    my_avg_overall = fields.Float(compute='_compute_my_stats')

    # Leaves
    my_pending_leaves = fields.Integer(compute='_compute_my_stats')
    my_approved_leaves = fields.Integer(compute='_compute_my_stats')
    my_total_leave_days = fields.Integer(compute='_compute_my_stats')

    # Expenses
    my_total_expenses = fields.Float(compute='_compute_my_stats')
    my_pending_expenses = fields.Float(compute='_compute_my_stats')

    # Tickets
    my_open_tickets = fields.Integer(compute='_compute_my_stats')
    my_resolved_tickets = fields.Integer(compute='_compute_my_stats')

    @api.depends('employee_id')
    def _compute_name(self):
        for r in self:
            r.name = f'Dashboard — {r.employee_id.name}' if r.employee_id else 'My Dashboard'

    def _compute_my_stats(self):
        today = datetime.now().date()
        for r in self:
            emp = r.employee_id
            if not emp:
                continue

            tasks = self.env['project.task'].search([('user_ids', 'in', emp.user_id.ids)]) if emp.user_id else self.env['project.task']

            r.my_total_tasks = len(tasks)
            r.my_todo = len(tasks.filtered(lambda t: t.custom_stage == 'todo'))
            r.my_in_progress = len(tasks.filtered(lambda t: t.custom_stage == 'in_progress'))
            r.my_in_review = len(tasks.filtered(lambda t: t.custom_stage == 'in_review'))
            r.my_approved = len(tasks.filtered(lambda t: t.custom_stage == 'approved'))
            r.my_rejected = len(tasks.filtered(lambda t: t.custom_stage == 'rejected'))
            r.my_overdue = len(tasks.filtered(
                lambda t: t.date_deadline and t.date_deadline < today and t.custom_stage not in ('approved', 'rejected')
            ))

            evals = self.env['artemis.evaluation'].search([('employee_id', '=', emp.id)])
            r.my_total_evaluations = len(evals)
            r.my_avg_overall = round(sum(e.overall_rating for e in evals) / len(evals), 2) if evals else 0

            leaves = self.env['artemis.leave'].search([('employee_id', '=', emp.id)])
            r.my_pending_leaves = len(leaves.filtered(lambda l: l.state == 'draft'))
            r.my_approved_leaves = len(leaves.filtered(lambda l: l.state == 'approved'))
            r.my_total_leave_days = sum(leaves.filtered(lambda l: l.state == 'approved').mapped('duration'))

            expenses = self.env['artemis.expense'].search([('employee_id', '=', emp.id)])
            r.my_total_expenses = sum(expenses.mapped('amount'))
            r.my_pending_expenses = sum(expenses.filtered(lambda e: e.state == 'draft').mapped('amount'))

            tickets = self.env['artemis.ticket'].search(
                ['|', ('requester_id', '=', emp.id), ('assigned_to_id', '=', emp.id)]
            )
            r.my_open_tickets = len(tickets.filtered(lambda t: t.state in ('new', 'in_progress')))
            r.my_resolved_tickets = len(tickets.filtered(lambda t: t.state == 'resolved'))

    def action_refresh(self):
        self._compute_my_stats()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'artemis.employee.dashboard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'main',
        }
