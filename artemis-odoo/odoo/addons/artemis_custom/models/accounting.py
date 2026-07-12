from odoo import models, fields, api


class ArtemisProjectBudget(models.Model):
    _name = 'artemis.project.budget'
    _description = 'Project Budget'
    _rec_name = 'project_id'

    project_id = fields.Many2one('project.project', string='Project', required=True)
    estimated_revenue = fields.Monetary(string='Estimated Revenue', currency_field='currency_id')
    estimated_cost = fields.Monetary(string='Estimated Cost')
    estimated_profit = fields.Monetary(string='Estimated Profit', compute='_compute_estimated')
    estimated_margin = fields.Float(string='Estimated Margin (%)', compute='_compute_estimated')

    actual_revenue = fields.Monetary(string='Actual Revenue', compute='_compute_actual', currency_field='currency_id')
    actual_cost = fields.Monetary(string='Actual Cost', compute='_compute_actual')
    actual_profit = fields.Monetary(string='Actual Profit', compute='_compute_actual')
    actual_margin = fields.Float(string='Actual Margin (%)', compute='_compute_actual')

    expense_ids = fields.One2many('artemis.expense', 'budget_id', string='Expenses')
    invoice_ids = fields.One2many('artemis.invoice', 'budget_id', string='Invoices')

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft')

    @api.depends('estimated_revenue', 'estimated_cost')
    def _compute_estimated(self):
        for r in self:
            rev = r.estimated_revenue or 0
            cost = r.estimated_cost or 0
            r.estimated_profit = rev - cost
            r.estimated_margin = round((rev - cost) / rev * 100, 1) if rev > 0 else 0

    @api.depends('expense_ids', 'invoice_ids')
    def _compute_actual(self):
        for r in self:
            rev = sum(r.invoice_ids.filtered(lambda x: x.state == 'paid').mapped('amount'))
            cost = sum(r.expense_ids.filtered(lambda x: x.state == 'approved').mapped('amount'))
            r.actual_revenue = rev
            r.actual_cost = cost
            r.actual_profit = rev - cost
            r.actual_margin = round((rev - cost) / rev * 100, 1) if rev > 0 else 0

    def action_activate(self):
        self.state = 'active'

    def action_close(self):
        self.state = 'closed'


class ArtemisExpense(models.Model):
    _name = 'artemis.expense'
    _description = 'Expense'
    _rec_name = 'description'
    _order = 'date desc'

    budget_id = fields.Many2one('artemis.project.budget', string='Budget')
    project_id = fields.Many2one('project.project', string='Project', related='budget_id.project_id', store=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    category = fields.Selection([
        ('travel', 'Travel'),
        ('software', 'Software & Licenses'),
        ('hardware', 'Hardware'),
        ('cloud', 'Cloud Services'),
        ('office', 'Office Supplies'),
        ('other', 'Other'),
    ], string='Category', default='other')
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    description = fields.Text(string='Description')
    receipt = fields.Binary(string='Receipt')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft')

    def action_approve(self):
        self.state = 'approved'

    def action_reject(self):
        self.state = 'rejected'


class ArtemisInvoice(models.Model):
    _name = 'artemis.invoice'
    _description = 'Invoice'
    _rec_name = 'number'
    _order = 'date desc'

    budget_id = fields.Many2one('artemis.project.budget', string='Budget')
    project_id = fields.Many2one('project.project', string='Project', related='budget_id.project_id', store=True)
    number = fields.Char(string='Invoice Number', required=True)
    client_name = fields.Char(string='Client Name')
    amount = fields.Monetary(string='Amount', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    date = fields.Date(string='Date', required=True, default=fields.Date.today)
    due_date = fields.Date(string='Due Date')
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ], string='Status', default='draft')

    def action_send(self):
        self.state = 'sent'

    def action_mark_paid(self):
        self.state = 'paid'
