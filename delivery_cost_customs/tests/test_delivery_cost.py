# -*- coding: utf-8 -*-

from odoo.tests import common, Form
from odoo.tools import float_compare

class TestDeliveryCustomsCost(common.TransactionCase):

    def setUp(self):
        super(TestDeliveryCustomsCost, self).setUp()
        self.SaleOrder = self.env['sale.order']
        self.SaleOrderLine = self.env['sale.order.line']
        self.partner_18 = self.env.ref('base.res_partner_18')
        self.partner_18.write({
            "country_id": self.env.ref('base.pe').id
        })
        self.pricelist = self.env.ref('product.list0')
        self.product_4 = self.env.ref('product.product_product_4')

        # as the tests hereunder assume all the prices in USD, we must ensure
        # that the company actually uses USD
        self.env.cr.execute(
            "UPDATE res_company SET currency_id = %s WHERE id = %s",
            [self.env.ref('base.USD').id, self.env.user.company_id.id])
        self.pricelist.currency_id = self.env.ref('base.USD').id

        self.normal_delivery = self.env.ref('delivery.normal_delivery_carrier')
        self.normal_delivery.write({
            'customs_require': True,
            'customs_cost': 110,
            'customs_amount': 3000
        })

    def test_01_delivery_cost(self):
        """Test add customs cost in delivery"""
        order = self.SaleOrder.create({
            'partner_id': self.partner_18.id,
            'partner_invoice_id': self.partner_18.id,
            'partner_shipping_id': self.partner_18.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [(0, 0, {
                'name': 'PC Assamble + 2GB RAM',
                'product_id': self.product_4.id,
                'product_uom_qty': 1,
                'price_unit': 3000.00,
            })],
            'carrier_id': self.normal_delivery.id
        })

        # I add delivery cost in Sales order
        delivery_wizard = Form(self.env['choose.delivery.carrier'].with_context({
            'default_order_id': order.id,
            'default_carrier_id': self.normal_delivery.id
        }))
        choose_delivery_carrier = delivery_wizard.save()
        choose_delivery_carrier.button_confirm()

        # I check sales order after added delivery cost
        line = self.SaleOrderLine.search([('order_id', '=', order.id),
            ('product_id', '=', self.normal_delivery.product_id.id)])

        self.assertEqual(len(line), 1, "Delivery cost is not Added")

        self.assertEqual(float_compare(line.price_subtotal, 120.0, precision_digits=2), 0,
                         "Delivery cost is not correspond.")
