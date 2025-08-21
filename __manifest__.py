# -*- coding: utf-8 -*-
{
    'name': "simple_library",

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
    'depends': ['base', 'report_xlsx'],

    # always loaded
    'data': [
        # data
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        #reports
        'reports/peminjaman_report_excel_action.xml',
        'reports/library_report_paperformat.xml',
        'reports/library_report_action.xml',
        'reports/library_report_template.xml',
        'reports/peminjaman_report_paperformat.xml',
        'reports/peminjaman_report_action.xml',
        'reports/peminjaman_report_template.xml',
        'reports/pengembalian_report_paperformat.xml',
        'reports/pengembalian_report_action.xml',
        'reports/pengembalian_report_template.xml',
        # views
        'views/views.xml',
        'views/templates.xml',
        'views/booksview.xml',
        'views/logbooksview.xml',
        'views/peopleview.xml',
        'views/borrowview.xml',
        'views/givebackview.xml',
        'views/fineview.xml',
        'views/contactview.xml',
        'views/penulis.xml',
        'views/penerbit.xml',
        #wizard
        'wizard/borrow_report_wizard_views.xml',
        'wizard/borrow_report_wizard_actions.xml',
        'wizard/minjam.xml',
        'wizard/giveback_report_wizard_views.xml',
        'wizard/giveback_report_wizard_actions.xml',
        'wizard/balikin.xml',
        #menu
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

