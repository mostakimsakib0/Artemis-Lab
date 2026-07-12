from odoo import models, fields, api
from datetime import timedelta


class ArtemisContract(models.Model):
    _name = 'artemis.contract'
    _description = 'Employment Contract'
    _rec_name = 'employee_id'
    _order = 'start_date desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    type = fields.Selection([
        ('permanent', 'Permanent'),
        ('probation', 'Probation'),
        ('intern', 'Intern'),
        ('contractual', 'Contractual'),
    ], string='Contract Type', default='permanent')
    start_date = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    end_date = fields.Date(string='End Date')
    salary = fields.Monetary(string='Salary', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ], string='Status', default='draft')

    active = fields.Boolean(default=True)

    def action_activate(self):
        self.state = 'active'

    def action_expire(self):
        self.state = 'expired'


class ArtemisLeave(models.Model):
    _name = 'artemis.leave'
    _description = 'Leave Request'
    _rec_name = 'employee_id'
    _order = 'date_from desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    type = fields.Selection([
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('personal', 'Personal Leave'),
    ], string='Leave Type', required=True)
    date_from = fields.Date(string='From', required=True)
    date_to = fields.Date(string='To', required=True)
    duration = fields.Integer(string='Duration (Days)', compute='_compute_duration')
    reason = fields.Text(string='Reason')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft')

    @api.depends('date_from', 'date_to')
    def _compute_duration(self):
        for r in self:
            if r.date_from and r.date_to:
                r.duration = (r.date_to - r.date_from).days + 1
            else:
                r.duration = 0

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'


class ArtemisPayslip(models.Model):
    _name = 'artemis.payslip'
    _description = 'Payslip'
    _rec_name = 'employee_id'
    _order = 'date_from desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    contract_id = fields.Many2one('artemis.contract', string='Contract')
    date_from = fields.Date(string='Period From', required=True)
    date_to = fields.Date(string='Period To', required=True)

    basic_salary = fields.Monetary(string='Basic Salary', currency_field='currency_id')
    house_rent = fields.Monetary(string='House Rent')
    medical = fields.Monetary(string='Medical Allowance')
    conveyance = fields.Monetary(string='Conveyance')
    other_allowances = fields.Monetary(string='Other Allowances')

    gross_salary = fields.Monetary(string='Gross Salary', compute='_compute_totals')
    tax_deduction = fields.Monetary(string='Tax Deduction')
    other_deductions = fields.Monetary(string='Other Deductions')
    net_pay = fields.Monetary(string='Net Pay', compute='_compute_totals')

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
    ], string='Status', default='draft')

    @api.depends('basic_salary', 'house_rent', 'medical', 'conveyance', 'other_allowances', 'tax_deduction', 'other_deductions')
    def _compute_totals(self):
        for r in self:
            r.gross_salary = (r.basic_salary or 0) + (r.house_rent or 0) + (r.medical or 0) + (r.conveyance or 0) + (r.other_allowances or 0)
            r.net_pay = r.gross_salary - (r.tax_deduction or 0) - (r.other_deductions or 0)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_pay(self):
        self.state = 'paid'

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        today = fields.Date.today()
        first = today.replace(day=1)
        last = (first + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        if 'date_from' in fields:
            res['date_from'] = first
        if 'date_to' in fields:
            res['date_to'] = last
        return res
