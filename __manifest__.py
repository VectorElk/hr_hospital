{
    'name': 'HR Hospital',
    'summary': 'HR Hospital module for odoo.school',
    'author': 'Ihor Los',
    'website': 'https://odoo.school/',
    'category': 'Human Resources',
    'license': 'OPL-1',
    'version': '19.0.0.0.0',

    'data': [
        'security/ir.model.access.csv',
        'data/hr_hospital_condition_data.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_condition_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_main_menu.xml',
    ],

    'demo': [
        'demo/hr_hospital_demo.xml',
    ],

    'icon': 'hr_hospital/static/description/icon.png',
}