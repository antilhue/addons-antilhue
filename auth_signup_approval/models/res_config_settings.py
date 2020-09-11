from odoo import fields, models


class res_config_settings(models.TransientModel):

    _inherit = "res.config.settings"

    notify_signup_user_ids = fields.Many2many(relation="res.users", string="Notified users when a user sign up",
                                              related='company_id.notify_signup_user_ids', readonly=False)
