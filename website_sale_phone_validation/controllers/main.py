from odoo import _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo.addons.phone_validation.tools import phone_validation
from odoo.exceptions import UserError


class WebsiteSale(WebsiteSale):

    def values_postprocess(self, order, mode, values, errors, error_msg):
        """Customer phone set with correct format"""
        new_values, errors, error_msg = super(WebsiteSale, self).values_postprocess(order, mode, values, errors,
                                                                                    error_msg)
        if values.get('phone') and values.get('country_id'):
            country = request.env['res.country'].browse(int(values.get('country_id')))
            new_values['phone'] = phone_validation.phone_format(
                values.get('phone'), country.code, country.phone_code, raise_exception=False)
        return new_values, errors, error_msg

    def checkout_form_validate(self, mode, all_form_values, data):
        """Validate that phone is write correctly"""
        error, error_message = super(WebsiteSale, self).checkout_form_validate(mode, all_form_values, data)
        if data.get('phone') and data.get('country_id'):
            country = request.env['res.country'].browse(int(data.get('country_id')))
            try:
                phone_validation.phone_parse(data.get('phone'), country.code)
            except UserError:
                error["phone"] = 'error'
                error_message.append(_('Invalid Phone! Please enter a valid phone.'))

        return error, error_message


