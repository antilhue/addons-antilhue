{
    'name': 'Algolia based Autocomplete',
    'category': 'Website',
    'version': '1.0.0',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/search.xml',
        'views/res_config_settings.xml',
        'views/service_algolia.xml',
    ],
    'demo': [
        'demo/service_algolia_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'OPL-1',
    'author': "Antilhue",
}