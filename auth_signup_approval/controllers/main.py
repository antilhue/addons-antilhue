import logging
import werkzeug

from odoo import _, SUPERUSER_ID
from odoo.http import request, route
from odoo.exceptions import UserError
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.auth_signup.controllers.main import AuthSignupHome


_logger = logging.getLogger(__name__)

try:
    from email_validator import validate_email, EmailSyntaxError, \
        EmailUndeliverableError
except ImportError:
    # pragma: no-cover
    try:
        from validate_email import validate_email as _validate

        class EmailSyntaxError(Exception):
            message = False

        class EmailUndeliverableError(Exception):
            message = False

        def validate_email(*args, **kwargs):
            if not _validate(*args, **kwargs):
                raise EmailSyntaxError

    except ImportError:
        _logger.debug("Cannot import `email_validator`.")
    else:
        _logger.warning("Install `email_validator` to get full support.")


class SignupVerifyEmail(AuthSignupHome):

    @route()
    def web_auth_signup(self, *args, **kw):
        if request.params.get("login") and request.params.get("password"):
            return super(SignupVerifyEmail, self).web_auth_signup(*args, **kw)

        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                qcontext["message_signup"] = True
                return request.render("auth_signup.reset_password", qcontext)
            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    @staticmethod
    def check_format_email(login):
        try:
            validate_email(login or "")
        except EmailSyntaxError:
            raise UserError(_("That does not seem to be an email address."))
        except (EmailUndeliverableError, Exception) as e:
            raise UserError(str(e))

    def do_signup(self, qcontext):
        self.check_format_email(qcontext.get('login', ''))
        return super(SignupVerifyEmail, self).do_signup(qcontext)

    def _signup_with_values(self, token, values):
        values['password'] = values.get('password') or ''
        values.update({'geoip': request.session.get('geoip', {})})
        db, login, password = request.env['res.users'].sudo().signup(values, token)
        request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
        if password:
            uid = request.session.authenticate(db, login, password)
            if not uid:
                raise SignupError(_('Authentication Failed.'))

