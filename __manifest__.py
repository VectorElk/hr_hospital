# ruff: noqa: B018
{
    'name': 'HR Hospital',
    'summary': 'HR Hospital module for odoo.school',
    'description': '''
Hospital management addon for Odoo School.

This module provides hospital patient, doctor, visit, and condition management,
plus reporting, role-based access, and Ukrainian translations.
    ''',
    'author': 'Ihor Los',
    'website': 'https://odoo.school/',
    'category': 'Human Resources',
    'license': 'OPL-1',
    'version': '19.0.3.0.0',
    'depends': [
        'base',
    ],

    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_rules.xml',
        'data/hr_hospital_condition_data.xml',
        'report/hr_hospital_doctor_report_templates.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_condition_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_main_menu.xml',
        'wizard/hr_hospital_mass_reassign_doctor_wizard_views.xml',
        'wizard/hr_hospital_visit_report_wizard_views.xml',
    ],

    'demo': [
        'demo/hr_hospital_demo.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,

    'icon': 'hr_hospital/static/description/icon.png',
    'images': [
        'static/description/icon.png',
        'static/description/banner.svg',
    ],
}