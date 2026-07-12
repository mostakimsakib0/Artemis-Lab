from odoo import models, fields


class ArtemisDocumentFolder(models.Model):
    _name = 'artemis.document.folder'
    _description = 'Artemis Document Folder'

    name = fields.Char(string='Folder Name', required=True)
    project_id = fields.Many2one('project.project', string='Project', required=True)
    folder_type = fields.Selection(
        [('srs', 'SRS'), ('design', 'Design'), ('reports', 'Reports'), ('final', 'Final')],
        string='Folder Type'
    )
    parent_id = fields.Many2one('artemis.document.folder', string='Parent Folder')
    description = fields.Text('Description')
