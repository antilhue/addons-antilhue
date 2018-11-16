# coding: utf-8
from unittest.mock import patch, MagicMock, Mock
from odoo.tests.common import TransactionCase


class ServiceAlgoliaTestCase(TransactionCase):

    def setUp(self):
        super(ServiceAlgoliaTestCase, self).setUp()
        self.service_algolia = self.env.ref('website_sale_algolia.service_algolia_demo')
        self.website = self.env.ref('website.default_website').service_algolia_id = self.service_algolia
        self.ipod_product = self.env.ref('product.product_product_11b_product_template')
        self.pc_product = self.env.ref('product.product_product_3_product_template')

    @patch('algoliasearch.index.Index.add_objects')
    def test_write_product(self, request_algolia):
        request_algolia.return_value = True
        self.ipod_product.name = 'Test1'
        dict_values = {
            'objectID': self.ipod_product.id,
            'name': self.ipod_product.name,
            'default_code': self.ipod_product.default_code}
        request_algolia.assert_called_with([dict_values])

    @patch('algoliasearch.index.Index.add_objects')
    def test_write_product_extra_field(self, request_algolia):
        request_algolia.return_value = True
        self.service_algolia.algolia_fields = 'name,default_code,description'
        self.ipod_product.description = 'Test Description'
        dict_values = {
            'objectID': self.ipod_product.id,
            'name': self.ipod_product.name,
            'default_code': self.ipod_product.default_code,
            'description': self.ipod_product.description}
        request_algolia.assert_called_with([dict_values])

    @patch('algoliasearch.index.Index.add_objects')
    def test_write_product_wrong_fields_algolia(self, request_algolia):
        request_algolia.return_value = True
        self.ipod_product.name = 'Test1'
        self.service_algolia.algolia_fields = 'name,default_code,wrong_field'
        dict_values = {
            'objectID': self.ipod_product.id,
            'name': self.ipod_product.name,
            'default_code': self.ipod_product.default_code}
        request_algolia.assert_called_with([dict_values])

    @patch('algoliasearch.index.Index.add_objects')
    def test_write_published_product(self, request_algolia):
        request_algolia.return_value = True
        self.pc_product.website_published = True
        dict_values = {
            'objectID': self.pc_product.id,
            'name': self.pc_product.name,
            'default_code': self.pc_product.default_code}
        request_algolia.assert_called_with([dict_values])

    @patch('algoliasearch.index.Index.delete_objects')
    @patch('algoliasearch.index.Index.add_objects')
    def test_create_and_unlink_product_published(self, add_algolia, delete_algolia):
        # Create
        add_algolia.return_value = True
        product = self.env['product.template'].create({'name': 'Test_create', 'website_published': True})
        dict_values = {
            'objectID': product.id,
            'name': product.name,
            'default_code': product.default_code}
        add_algolia.assert_called_with([dict_values])

        # Unlink
        product_ids = product.ids
        delete_algolia.return_value = True
        product.unlink()
        delete_algolia.assert_called_with(product_ids)

    @patch('algoliasearch.index.Index.delete_objects')
    def test_unpublished_product(self, delete_algolia):
        delete_algolia.return_value = True
        self.ipod_product.website_published = False
        delete_algolia.assert_called_with(self.ipod_product.ids)

    @patch('algoliasearch.index.Index.delete_objects')
    def test_inactive_product(self, delete_algolia):
        delete_algolia.return_value = True
        self.ipod_product.active = False
        delete_algolia.assert_called_with(self.ipod_product.ids)



