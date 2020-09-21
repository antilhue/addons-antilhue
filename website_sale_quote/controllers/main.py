from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleQuote(WebsiteSale):

    @http.route(['/shop/quote'], type='http', auth="public", website=True)
    def quote(self, **post):
        order = request.website.sale_get_order()
        if order.env.su:
            # sending mail in sudo was meant for it being sent from superuser
            order = order.with_user(SUPERUSER_ID)
        email_act = order.action_quotation_send()
        if email_act and email_act.get('context'):
            email_ctx = email_act.get('context', {})
            order.with_context(email_ctx).message_post_with_template(
                email_ctx.get('default_template_id'),composition_mode='comment',
                email_layout_xmlid="mail.mail_notification_paynow")
            request.website.sale_reset()
            return request.redirect(order.get_portal_url())
        return request.render('website_sale_quote.confirmation_order_error')

    @http.route(['/shop/quote/redirect'], type='http', auth="public", website=True)
    def redirect_saleorder(self):
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            return request.redirect(order.get_portal_url())
        else:
            return request.redirect('/shop')
