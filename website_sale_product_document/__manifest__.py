{
    'name': 'Product documents published on the Website',
    'category': 'Website',
    'version': '14.0.1.0.0',
    'depends': ['website_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/templates.xml',
        'views/ir_attachment_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'license': 'OPL-1',
    'author': "Antilhue",
}