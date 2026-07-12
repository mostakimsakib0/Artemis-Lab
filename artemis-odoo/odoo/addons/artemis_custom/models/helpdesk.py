from odoo import models, fields, api


class ArtemisTicket(models.Model):
    _name = 'artemis.ticket'
    _description = 'Support Ticket'
    _rec_name = 'name'
    _order = 'priority desc, create_date desc'

    name = fields.Char(string='Subject', required=True)
    description = fields.Text(string='Description')
    category = fields.Selection([
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('support', 'Support'),
        ('general', 'General'),
    ], string='Category', default='general')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical'),
    ], string='Priority', default='1')
    requester_id = fields.Many2one('hr.employee', string='Requester', required=True)
    assigned_to_id = fields.Many2one('hr.employee', string='Assigned To')
    project_id = fields.Many2one('project.project', string='Project')
    state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='new')
    deadline = fields.Date(string='Deadline')
    resolution = fields.Text(string='Resolution Notes')
    color = fields.Integer(string='Color Index')

    def action_assign(self):
        self.state = 'in_progress'

    def action_resolve(self):
        self.state = 'resolved'

    def action_close(self):
        self.state = 'closed'

    def action_reopen(self):
        self.state = 'new'
