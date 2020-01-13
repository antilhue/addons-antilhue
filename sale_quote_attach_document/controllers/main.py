# -*- coding: utf-8 -*-

import base64
import werkzeug
from odoo import exceptions, fields, http, _
from odoo.http import request
from odoo.exceptions import AccessError, MissingError
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortal(CustomerPortal):

    @http.route(['/my/orders/<int:order_id>/attach'], type='http', auth="public", methods=['POST'], website=True)
    def attach_document(self, order_id, access_token=None, **post):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        message = post.get('attach_message', '')
        file = post.get('a_document')
        reference = post.get('client_order_ref', '')
        if not file:
            return werkzeug.utils.redirect("/my/orders/%s?access_token=%s" % (order_id, access_token))

        attachment_value = {
            'name': file.filename,
            'datas': base64.encodebytes(file.read()),
            'datas_fname': file.filename,
            'res_model': 'sale.order',
            'res_id': order_sudo.id,
        }
        attachment_id = request.env['ir.attachment'].sudo().create(attachment_value)

        values = {
            'body': _("<p> Reference:  %s </p> <p> %s </p>") % (reference, message),
            'model': 'sale.order',
            'message_type': 'comment',
            'no_auto_thread': False,
            'res_id': order_id,
            'subtype_id': request.env.ref('mail.mt_comment').id,
            'attachment_ids': [(6, 0, [attachment_id.id])],
            'author_id': request.env.user.partner_id.id
        }
        request.env['mail.message'].sudo().create(values)
        return werkzeug.utils.redirect(order_sudo.get_portal_url(query_string='&message=attach_ok'))
