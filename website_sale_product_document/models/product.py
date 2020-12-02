from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    document_website_ids = fields.One2many('product.document', 'product_id', string='Documents', copy=True, auto_join=True)

class ProductDocument(models.Model):
    _name = "product.document"
    _description = "Product Document"
    _order = "sequence, id"

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(related='attachment_id.document_name')
    attachment_id = fields.Many2one('ir.attachment', string='File', domain=[('res_id', '=', False),('mimetype','=','application/pdf')])
    product_id = fields.Many2one('product.template', string='Product Reference', required=True, ondelete='cascade', index=True, copy=False)
    description = fields.Text(related='attachment_id.description')
