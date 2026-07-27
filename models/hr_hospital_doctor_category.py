from odoo import fields, models


class HrHospitalDoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Hospital Doctor Qualification Category'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    res_doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='res_doctor_category_id',
    )

    _name_uniq = models.Constraint(
        'unique(name)',
        'The name of the doctor category must be unique.',
    )
