from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    """Removing Provinces of res.country.state and replacing provinces by regions"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    cr.execute("""
    SELECT state.id, region.name FROM (
        SELECT id, l10n_cl_region_id 
            FROM res_country_state 
            WHERE country_id = (
                SELECT id FROM res_country WHERE code='CL') 
            AND code LIKE 'CL%') AS state 
            INNER JOIN
        res_country_state_region AS region
        ON state.l10n_cl_region_id = region.id; 
        """)

    for state in env.cr.dictfetchall():
        partners = env['res.partner'].search([("state_id", "=", state.get('id'))])
        if not partners:
            continue
        region = env['res.country.state'].search(
            [("name", "=", state.get('name')), ("code", "not like", "CL")], limit=1)
        partners.write({"state_id": region.id})

        cities = env['res.city'].search([("state_id", "=", state.get("id"))])
        if not cities:
            continue
        cities.write({"state_id": region.id})



