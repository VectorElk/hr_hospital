from odoo import fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.medic.info'
    _description = 'Hospital Patient'

    name = fields.Char(required=True)
    emergency_contact = fields.Char()
    insurance_contact = fields.Char()
    insurance_policy_number = fields.Char(size=20)

    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
    )

    personal_doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.history',
        inverse_name='res_patient_id',
    )

    family_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        domain=[('is_family_doctor', '=', True)],
    )

    res_visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='res_patient_id',
    )
