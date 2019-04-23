from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleQuote(WebsiteSale):

    @http.route(['/shop/quote'], type='http', auth="public", website=True)
    def quote(self, **post):
        order = request.website.sale_get_order()
        if order.force_quotation_send():
            request.website.sale_reset()
            return request.redirect('/shop/confirmation')

        return request.render(
            'website_sale_quote.confirmation_order_error')

    @http.route()
    def payment_get_status(self, sale_order_id, **post):
        order = request.env['sale.order'].sudo().browse(sale_order_id).exists()
        if order.payment_acquirer_id:
            return super(WebsiteSaleQuote, self).payment_get_status(
                sale_order_id, **post)

        return {
            'recall': True,
            'message': request.env['ir.ui.view'].render_template("website_sale_quote.order_state_message", {
                'order': order
            })
        }
