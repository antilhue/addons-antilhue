# -*- encoding: utf-8 -*-
from odoo import models, fields


class ResStateRegion(models.Model):
    _name = 'res.country.state.region'
    _description = "State Region"

    name = fields.Char(
            string='Region Name',
            help='The state code.',
            required=True,
        )
    code = fields.Char(
            string='Region Code',
            help='The region code.',
            required=True,
        )
    child_ids = fields.One2many(
            'res.country.state',
            'l10n_cl_region_id',
            string='Child Regions',
    )
