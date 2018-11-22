from odoo import api, fields, models, _
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _apply_action_algolia(self, action):
        website = self.env['website'].get_current_website()
        algolia = website.service_algolia_id
        if not algolia:
            return True
        if action == 'update':
            return algolia.add_objects_in_algolia(self)
        return algolia.delete_objects_in_algolia(self)

    def update_products_algolia(self):
        return self._apply_action_algolia('update')

    def delete_products_algolia(self):
        return self._apply_action_algolia('delete')

    @api.multi
    def write(self, values):
        """Update in Sevice Algolia"""
        res = super(ProductTemplate, self).write(values)
        if self._required_remove_in_algolia(values):
            self.delete_products_algolia()
            return res
        if self._required_modify_in_algolia(values):
            self.update_products_algolia()
        return res

    @staticmethod
    def _required_remove_in_algolia(values):
        return not values.get('website_published', True) or not values.get('active', True)

    def _required_modify_in_algolia(self, values):
        website = self.env['website'].get_current_website()
        fields_algolia = (website.service_algolia_id.algolia_fields or '').split(',')
        fields_algolia.extend(['website_published', 'name'])
        return any([f in values for f in fields_algolia])

    @api.multi
    def unlink(self):
        product_publish = self.filtered(lambda p: p.website_published)
        if product_publish:
            product_publish.delete_products_algolia()
        return super(ProductTemplate, self).unlink()

    @api.model
    def create(self, vals):
        template = super(ProductTemplate, self).create(vals)
        if template.website_published:
            template.update_products_algolia()
        return template
