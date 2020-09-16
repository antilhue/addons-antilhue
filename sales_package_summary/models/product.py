from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    length = fields.Float(digits='Stock Weight', help='Length of product in cm', related='product_variant_ids.length')
    height = fields.Float(digits='Stock Weight', help='Height of product in cm', related='product_variant_ids.height')
    width = fields.Float(digits='Stock Weight', help='Width of product in cm', related='product_variant_ids.width')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    length = fields.Float()
    height = fields.Float()
    width = fields.Float()
