# -*- coding: utf-8 -*-

import base64
import werkzeug
from odoo import exceptions, fields, http, _
from odoo.http import request


class SaleQuote(http.Controller):

    @http.route(['/quote/<int:order_id>/<token>/attach'], type='http', auth="public", methods=['POST'], website=True)
    def attach_document(self, order_id, token, **post):
        order = request.env['sale.order'].sudo().browse(order_id)
        if token != order.access_token:
            return request.render('website.404')
        message = post.get('attach_message', '')
        file = post.get('a_document')
        reference = post.get('client_order_ref', '')

        if not file:
            return werkzeug.utils.redirect("/quote/%s/%s" % (order_id, token))

        attachment_value = {
            'name': file.filename,
            'datas': base64.encodestring(file.read()),
            'datas_fname': file.filename,
            'res_model': 'sale.order',
            'res_id': order.id,
        }
        attachment_id = request.env['ir.attachment'].sudo().create(attachment_value)

        values = {
            'body': _("<p> Reference:  %s </p> <p> %s </p>") % (reference, message),
            'model': 'sale.order',
            'message_type': 'comment',
            'no_auto_thread': False,
            'res_id': order.id,
            'subtype_id': request.env.ref('mail.mt_comment').id,
            'attachment_ids': [(6, 0, [attachment_id.id])],
            'author_id': request.env.user.partner_id.id
        }
        request.env['mail.message'].sudo().create(values)
        return werkzeug.utils.redirect("/quote/%s/%s?message=5" % (order_id, token))
