# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'USS Exceldownload',
    'version' : '1.0',
    'summary': 'Download Excel Button',
    'description': """
Download Excel Button
====================
    """,
    'author' : 'Usha Deo',
    'category':'uss',
    'website': 'https://www.uss.net.in',
    'depends' : ['base'],
    'data': [
        'wizard/uss_download_excel_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
