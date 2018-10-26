# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    total_weight = fields.Float(string='Total Weight(kg)', compute='_compute_total_weight')
    total_volumen = fields.Float(string='Total Volumen(cm3)', compute='_compute_total_volumen')

    @api.multi
    @api.depends('order_line', 'order_line.product_uom_qty', 'order_line.product_uom_qty')
    def _compute_total_weight(self):
        for sale in self:
            # Only compute result when all products have weight
            if sale.order_line.filtered(
                    lambda l: not l.weight and l.product_id.type != 'service' and l.product_uom_qty > 0):
                sale.total_weight = -1
                continue
            sale.total_weight = sum(sale.order_line.mapped(lambda p: p.weight * p.product_uom_qty))

    @api.multi
    @api.depends('order_line', 'order_line.product_uom_qty', 'order_line.product_id')
    def _compute_total_volumen(self):
        for sale in self:
            # Only compute result when all products have weight
            if sale.order_line.filtered(
                    lambda l: not l.volumen and l.product_id.type != 'service' and l.product_uom_qty > 0):
                sale.total_volumen = -1
                continue
            sale.total_volumen = sum(sale.order_line.mapped(lambda p: p.volumen * p.product_uom_qty))


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    weight = fields.Float(string='Weight(kg)', related='product_id.weight', readonly=True)
    volumen = fields.Float(string='Volumen(cm3)', compute='_compute_volumen', readonly=True)

    @api.multi
    @api.depends('product_id', 'product_uom_qty')
    def _compute_volumen(self):
        for line in self:
            line.volumen = (line.product_id.length * line.product_id.height * line.product_id.width)
