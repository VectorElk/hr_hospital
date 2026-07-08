from odoo import fields, models


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(required=True)
    position = fields.Char(required=True)
    is_family_doctor = fields.Boolean(default=False)
    res_patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='family_doctor_id',
    )

    res_visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='res_doctor_id',
    )
