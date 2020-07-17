from odoo import api, fields, models, _


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    hide_attributes = fields.Boolean(help="Hide attributes filter on category")

