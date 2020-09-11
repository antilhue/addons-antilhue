from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    notify_signup_user_ids = fields.Many2many("res.users", string="Notified users when a user sign up" )