# -*- coding: utf-8 -*-
{
    'name': "STUDENT",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SAIAIPL",
    'website': "http://www.saiaipl.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/student_info_views.xml',
        'views/res_partner_views.xml',
        'views/support_ticket_views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    
}