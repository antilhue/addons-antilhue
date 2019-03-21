# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.tools.safe_eval import safe_eval


class res_config_settings(models.TransientModel):
    """
    Overwrite to add mail routing settings
    """
    _inherit = "res.config.settings"

    notify_signup_user_ids = fields.Many2many(
        "res.users",
        string="Notified users when a user sign up",
    )

    @api.model
    def get_values(self):
        """
        Overwrite to add new system params
        """
        res = super(res_config_settings, self).get_values()
        config = self.env['ir.config_parameter'].sudo()
        notify_signup_user_ids = safe_eval(config.get_param("notify_signup_user_ids", "[]"))
        values = {
            "notify_signup_user_ids": [(6, 0, notify_signup_user_ids)],
        }
        res.update(values)
        return res

    @api.model
    def set_values(self):
        """
        Overwrite to add new system params
        """
        super(res_config_settings, self).set_values()
        config = self.env['ir.config_parameter'].sudo()
        config.set_param("notify_signup_user_ids", self.notify_signup_user_ids.ids)
