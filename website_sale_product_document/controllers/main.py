# -*- coding: utf-8 -*-

import base64
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

import werkzeug


class WebsiteSale(WebsiteSale):

    @http.route(['/product/download/document',], type='http', auth='public')
    def download_product_document(self, document_id):
        document = request.env['product.document'].browse(int(document_id))
        if not document:
            return request.not_found()

        status, headers, content = request.env['ir.http'].binary_content(id=document.sudo().attachment_id)
        if status == 304:
            response = werkzeug.wrappers.Response(status=status, headers=headers)
        elif status == 301:
            return werkzeug.utils.redirect(content, code=301)
        elif status != 200:
            response = request.not_found()
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            headers.append((
                'Content-Disposition', "inline; filename*=UTF-8''%s" % document.sudo().attachment_id.name))
            response = request.make_response(content_base64, headers)

        return response


