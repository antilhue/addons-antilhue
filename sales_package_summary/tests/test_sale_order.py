# coding: utf-8

from odoo.tests.common import TransactionCase


class TestSaleOrder(TransactionCase):
    def setUp(self):
        super(TestSaleOrder, self).setUp()
        self.order_obj = self.env['sale.order']
        self.order_line_obj = self.env['sale.order.line']
        self.partner_id = self.env.ref('base.res_partner_2')
        self.product_lapto = self.env.ref('product.product_product_25')
        self.product_lapto.write({'length': 5, 'height': 5, 'width': 5, 'weight': 0.5})
        self.product_service = self.env.ref('sale.advance_product_0')
        self.product_service.write({'type': 'service'})
        self.product_imac = self.env.ref('product.product_product_8')
        self.product_imac.write({'length': 0, 'height': 0, 'width': 0, 'weight': 0})

    def test_001_add_product_in_saleorder(self):
        """Add products in sale order with or without dimensions"""
        sale_order = self.order_obj.create({'partner_id': self.partner_id.id})
        # Sale order without products
        self.assertEqual(round(sale_order.total_weight, 2), 0, "The total weight wrong, sale_order without lines")
        self.assertEqual(round(sale_order.total_volumen, 2), 0, "The total volumen wrong, sale_order without lines")
        # Add product with all dimensions
        self.create_order_line(sale_order, self.product_lapto)
        self.assertEqual(round(sale_order.total_weight, 2), 0.50, "The total weight not was correctly compute")
        self.assertEqual(round(sale_order.total_volumen, 6), 0.000125, "The total volumen not was correctly compute")
        # Increase the quantity of products and add s product of type = service
        sale_order.order_line.product_uom_qty = 5
        self.create_order_line(sale_order, self.product_service)
        self.assertEqual(round(sale_order.total_weight, 2), 0.50 * 5, "The total weight not was correctly compute")
        self.assertEqual(round(sale_order.total_volumen, 6), 0.000125 * 5, "The total volumen not was correctly compute")
        # Add a product without dimensions
        line = self.create_order_line(sale_order, self.product_imac)
        self.assertEqual(round(sale_order.total_weight, 2), -1, "The total weight not was correctly compute")
        self.assertEqual(round(sale_order.total_volumen, 2), -1, "The total volumen not was correctly compute")
        # Line qty=0
        line.product_uom_qty = 0
        self.assertEqual(round(sale_order.total_weight, 2), 0.50 * 5, "The total weight wrong, qty=0")
        self.assertEqual(round(sale_order.total_volumen, 6), 0.000125 * 5, "The total volumen wrong, qty=0")

    def create_order_line(self, order, product):
        return self.order_line_obj.create({
            'product_id': product.id,
            'product_uom_qty': 1,
            'order_id': order.id,
        })