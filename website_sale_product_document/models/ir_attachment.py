# -*- coding: utf-8 -*-

from odoo import models, fields


class IrAttachment(models.Model):
    _inherit = ['ir.attachment']

    document_name = fields.Char('Document Name')
