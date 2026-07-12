from odoo import models, fields, api
from odoo.exceptions import UserError


class CrmLostReasonWizard(models.TransientModel):
    _name = 'artemis.crm.lost.reason.wizard'
    _description = 'Lost Reason Wizard'

    lead_id = fields.Many2one('artemis.crm.lead', string='Lead', required=True)
    lost_reason = fields.Text(string='Lost Reason', required=True)

    def action_confirm_lost(self):
        if self.lead_id:
            self.lead_id.stage = 'lost'
            self.lead_id.lost_reason = self.lost_reason
            self.lead_id.probability = 0
