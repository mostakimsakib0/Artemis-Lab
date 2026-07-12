from odoo import models, fields, api


class ArtemisCrmLead(models.Model):
    _name = 'artemis.crm.lead'
    _description = 'CRM Lead'
    _rec_name = 'contact_name'
    _order = 'priority desc, create_date desc'

    contact_name = fields.Char(string='Contact Name', required=True)
    company_name = fields.Char(string='Company')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    source = fields.Selection([
        ('referral', 'Referral'),
        ('website', 'Website'),
        ('linkedin', 'LinkedIn'),
        ('cold_outreach', 'Cold Outreach'),
        ('conference', 'Conference / Event'),
        ('existing_client', 'Existing Client'),
        ('other', 'Other'),
    ], string='Source', default='other')
    service_ids = fields.Many2many('artemis.service', string='Services Interested')
    stage = fields.Selection([
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ], string='Stage', default='new', group_expand='_expand_stages')
    assigned_to_id = fields.Many2one('hr.employee', string='Assigned To')
    expected_revenue = fields.Monetary(string='Expected Revenue', currency_field='currency_id')
    probability = fields.Integer(string='Probability (%)', default=0)
    notes = fields.Text(string='Notes')
    lost_reason = fields.Text(string='Lost Reason')
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical'),
    ], string='Priority', default='1')
    communication_log = fields.One2many('artemis.crm.communication', 'lead_id', string='Communication Log')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    color = fields.Integer(string='Color Index')

    def _expand_stages(self, stages, domain, order):
        return ['new', 'contacted', 'qualified', 'proposal', 'won', 'lost']

    def action_set_stage(self, stage):
        self.stage = stage

    def action_mark_won(self):
        self.stage = 'won'
        self.probability = 100

    def action_mark_lost(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'artemis.crm.lost.reason.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lead_id': self.id},
        }


class ArtemisService(models.Model):
    _name = 'artemis.service'
    _description = 'Service'
    _rec_name = 'name'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)


class ArtemisCrmCommunication(models.Model):
    _name = 'artemis.crm.communication'
    _description = 'CRM Communication Log'
    _rec_name = 'subject'
    _order = 'date desc'

    lead_id = fields.Many2one('artemis.crm.lead', string='Lead', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    type = fields.Selection([
        ('email', 'Email'),
        ('call', 'Phone Call'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('other', 'Other'),
    ], string='Type', default='note')
    subject = fields.Char(string='Subject')
    body = fields.Text(string='Notes')
    employee_id = fields.Many2one('hr.employee', string='Logged By')
