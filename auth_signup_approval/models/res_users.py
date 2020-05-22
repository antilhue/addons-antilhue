# -*- coding: utf-8 -*-
import logging


from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    state = fields.Selection(
        selection=[('pending', 'Pending'), ('new', 'Never Connected'),
                   ('active', 'Confirmed'), ('rejected', 'Rejected')])
    approval_status = fields.Selection(
        [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    @api.multi
    def _compute_state(self):
        for user in self:
            user.state = 'active' if user.login_date else 'new'
            if not user.share or user.approval_status == 'approved':
                continue
            user.state = user.approval_status

    @api.multi
    def action_approval(self):
        self.write({'approval_status': 'approved'})
        self.action_reset_password()

    @api.multi
    def action_reject(self):
        self.write({'approval_status': 'rejected'})
        for user in self:
            template = self.env.ref('auth_signup_approval.user_signup_rejected')
            with self.env.cr.savepoint():
                template.with_context(
                    lang=user.lang).send_mail(user.id, force_send=True, raise_exception=True)

    @api.multi
    def notify_admin_user_signup(self, values):
        config = self.env['ir.config_parameter'].sudo()
        notify_user_id = safe_eval(config.get_param("notify_signup_user_ids", "[]"))
        if not notify_user_id:
            return True
        users = self.browse(notify_user_id)
        email_to = ','.join(users.mapped("email"))
        template = self.env.ref('auth_signup_approval.user_pending_approval')
        template.write({'email_to': email_to})

        for user in self:
            url = user.get_url_view_user()
            with self.env.cr.savepoint():
                template.with_context(
                    lang=user.company_id.partner_id.lang, url=url, city=values.get('city', ''), country_name=values.get('country_name', '')).send_mail(user.id, force_send=True, raise_exception=True)
            _logger.info("Notify Sing Up sent for user <%s> to <%s>", user.login, user.email)

    @api.multi
    def get_url_view_user(self):
        self.ensure_one()
        config = self.env['ir.config_parameter'].sudo()
        action = self.env.ref("base.action_res_users").id
        base_url = config.get_param('web.base.url')
        db = self.env.cr.dbname
        return "{}/web?db={}#id={}&view_type=form&model=res.users&action={}".format(base_url, db, self.id, action)

    @api.model
    def signup(self, values, token=None):
        cr, login, password = super(ResUsers, self).signup(values, token)
        if token:
            return cr, login, password

        users = self.search([('login', '=', login)])
        if not users:
            users = self.search([('email', '=', login)])
        if len(users) != 1:
            raise Exception(_('Notify Sign Up: invalid username or email'))

        users.notify_admin_user_signup(values.get("geoip", {}))

        return cr, login, password

    def reset_password(self, login):
        """ retrieve the user corresponding to login (login or email),
            and reset their password
        """
        users = self.search([('login', '=', login)])
        if not users:
            users = self.search([('email', '=', login)])
        if len(users) != 1 or (users.state != 'active' or users.approval_status == 'rejected'):
            raise Exception(_('Reset password: invalid username or email'))
        return users.action_reset_password()