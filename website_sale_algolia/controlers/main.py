# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http
from odoo.http import request


class WebsiteAlgolia(http.Controller):

    @http.route('/shop/get_algolia_settings/', type='json', auth='public', website=True)
    def get_translated_length(self):
        service = request.website.service_algolia_id
        if not service:
            return {}
        setting = {'app': service.algolia_app_id,
                   'key': service.algolia_key_search,
                   'index': service.algolia_index}
        return setting
