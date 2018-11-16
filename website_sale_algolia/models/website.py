from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'

    service_algolia_id = fields.Many2one(
        'service.algolia', string="Server Algolia")
