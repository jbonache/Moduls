# -*- coding: utf-8 -*-
{
    'name': "GalacticTribals",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'crons/cron.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/players.xml',
        'views/tribes.xml',
        'views/planets.xml',
        'views/resources.xml',
        'views/buildings.xml',
        'views/spaceships.xml',
        'views/battles.xml',
        'views/alliances.xml',
        'wizards/viewGenerarBatalla.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/galactic_tribals_demo.xml',
    ],
}

