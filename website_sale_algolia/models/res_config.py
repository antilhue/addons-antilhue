
from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    service_algolia_id = fields.Many2one(
        'service.algolia', related='website_id.service_algolia_id',
        string="Server Algolia", readonly=False,
        help="Algolia service to autocomplete product searches in the virtual store")

    def uptate_website_products_algolia(self):
        products = self.env['product.template'].search([("website_published", "=", True)])
        if not products:
            return False
        products.update_products_algolia()
