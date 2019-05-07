# -*- encoding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _


class res_state(models.Model):
    _inherit = 'res.country.state'

    l10n_cl_region_id = fields.Many2one(
            'res.country.state.region',
            string='Region',
            index=True,
        )