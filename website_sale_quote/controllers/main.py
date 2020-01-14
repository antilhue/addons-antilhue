from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleQuote(WebsiteSale):

    @http.route(['/shop/quote'], type='http', auth="public", website=True)
    def quote(self, **post):
        order = request.website.sale_get_order()
        if order and order.force_quotation_send():
            request.website.sale_reset()
            return request.redirect(order.get_portal_url())

        return request.render(
            'website_sale_quote.confirmation_order_error')

    @http.route(['/shop/quote/redirect'], type='http', auth="public", website=True)
    def redirect_saleorder(self):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            return request.redirect(order.get_portal_url())
        else:
            return request.redirect('/shop')
