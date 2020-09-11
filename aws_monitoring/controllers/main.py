import werkzeug
from odoo import http


class MonitoringAws(http.Controller):

    @http.route('/health', type='http', auth='none')
    def health(self):
        return werkzeug.wrappers.Response(status=200)
