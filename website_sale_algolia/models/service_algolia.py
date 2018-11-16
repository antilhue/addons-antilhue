from odoo import api, fields, models, _
from algoliasearch import algoliasearch
from algoliasearch.helpers import AlgoliaException
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ServiceAlgolia(models.Model):
    _name = 'service.algolia'

    name = fields.Char(required=True)
    algolia_app_id = fields.Char(
        'Application ID', required=True,
        help="This is your unique application identifier."
             "It's used to identify you when using Algolia's API.")
    algolia_key_search = fields.Char(
        'Search-Only API Key', help="This is the public API key to use in your frontend code."
                                    "This key is only usable for search queries.")
    algolia_key_admin = fields.Char(
        'Admin API Key', required=True,
        help="This is the ADMIN API key.This key is used to create,"
             " update and DELETE your indices. You can also use it to manage your API keys.")
    algolia_index = fields.Char('Index', required=True)
    algolia_fields = fields.Char(help="Comma-separated list of field names that store in algolia.")

    @api.multi
    def _init_index_algolia(self):
        """Return Index Object, in this point only the Index
        object is instantiated, not connect with Algolia"""
        self.ensure_one()
        try:
            client = algoliasearch.Client(self.algolia_app_id, self.algolia_key_admin)
            index = client.init_index(self.algolia_index)
        except ValueError as err:
            _logger.info(err)
            return False
        return index

    @api.multi
    def _algolia_fields_to_list(self):
        return (self.algolia_fields or '').split(',')

    @api.multi
    def execute(self, operation, records):
        """Execute an operation (add, delete) in the Algolia service,
        given in a set of records and return trueif the operation
        was successful or false otherwise.
        add --> add_objects
        delete --> delete_objects"""
        self.ensure_one()
        index = self._init_index_algolia()
        list_records = self._generate_values(records) if operation == 'update' else records.ids
        operators_algolia = {'update': index.add_objects, 'delete': index.delete_objects}
        try:
            method_algolia = operators_algolia.get(operation)
            method_algolia(list_records)
        except AlgoliaException as e:
            _logger.warning(e)
            return False
        return True

    def _generate_values(self, records):
        """Return dict with product data to update in Algolia,
        always it has name and ObjectID values"""
        object_list = []
        fields_list = self._algolia_fields_to_list()
        for each in records:
            value = {'objectID': each.id, 'name': each.name}
            for f in fields_list:
                # Omit wrong field
                try:
                    value[f] = each[f]
                except KeyError:
                    continue
            object_list.append(value)
        return object_list

    def test_algolia_connection(self):
        """Inform the user about the state of the connection with algolia"""
        client = algoliasearch.Client(self.algolia_app_id, self.algolia_key_admin)
        try:
            client.list_indexes()
        except AlgoliaException as e:
            raise UserError(_("Connection Test Failed!"))
        # TODO: This not would UserError, it most be Info
        raise UserError(_("Connection Test Succeeded! Everything seems properly set up!"))
