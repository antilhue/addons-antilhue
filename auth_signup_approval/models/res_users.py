import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    state = fields.Selection(selection_add=[('pending', 'Pending'), ('new', ), ('active', ), ('rejected', 'Rejected')])
    approval_status = fields.Selection(
        [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    def _compute_state(self):
        for user in self:
            user.state = 'active' if user.login_date else 'new'
            if not user.share or user.approval_status == 'approved':
                continue
            user.state = user.approval_status

    def action_approval(self):
        self.write({'approval_status': 'approved'})
        self.action_reset_password()

    def action_reject(self):
        self.write({'approval_status': 'rejected'})
        template = self.env.ref('auth_signup_approval.user_signup_rejected')
        for user in self:
            with self.env.cr.savepoint():
                template.with_context(
                    lang=user.lang).send_mail(user.id, force_send=True, raise_exception=True)

    def notify_admin_user_signup(self, values):
        template = self.env.ref('auth_signup_approval.user_pending_approval')
        for user in self:
            notify_user_ids = self.company_id.notify_signup_user_ids
            if not notify_user_ids:
                continue
            email_to = ','.join(notify_user_ids.mapped("email"))
            template.write({'email_to': email_to})
            url = user.get_url_view_user()
            with self.env.cr.savepoint():
                template.sudo().with_context(
                    lang=user.company_id.partner_id.lang,
                    url=url,
                    city=values.get('city', ''),
                    country_name=values.get('country_name', '')
                ).send_mail(user.id, force_send=True, raise_exception=True)
            _logger.info("Notify Sing Up sent for user <%s> to <%s>", user.login, user.email)

    def get_url_view_user(self):
        self.ensure_one()
        config = self.env['ir.config_parameter'].sudo()
        action = self.env.ref("base.action_res_users").id
        base_url = config.get_param('web.base.url')
        db = self.env.cr.dbname
        return "{}/web?db={}#id={}&view_type=form&model=res.users&action={}".format(base_url, db, self.id, action)

    @api.model
    def signup(self, values, token=None):
        geoip = values.pop('geoip', {})
        cr, login, password = super(ResUsers, self).signup(values, token)
        if token:
            return cr, login, password

        users = self.search(['|', ('login', '=', login), ('email', '=', login)])
        if len(users) != 1:
            raise Exception(_('Notify Sign Up: invalid username or email'))
        users.notify_admin_user_signup(geoip)

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