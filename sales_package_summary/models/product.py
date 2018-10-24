from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length = fields.Float(digits=dp.get_precision(
        'Stock Weight'), help='Length of product in cm', related='product_variant_ids.length')
    height = fields.Float(digits=dp.get_precision(
        'Stock Weight'), help='Height of product in cm', related='product_variant_ids.height')
    width = fields.Float(digits=dp.get_precision(
        'Stock Weight'), help='Width of product in cm', related='product_variant_ids.width')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
