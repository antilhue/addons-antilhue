# -*- encoding: utf-8 -*-
from odoo import fields, models, api
from odoo.tools.translate import _


class ResCity(models.Model):
    _inherit = 'res.city'

    l10n_cl_code = fields.Char(
            string='City Code',
            help='The city code.\n',
            required=True,
        )