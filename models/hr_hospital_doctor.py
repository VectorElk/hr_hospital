import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class HRHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(required=True)
    position = fields.Char(required=True)
    is_family_doctor = fields.Boolean(default=False)
    res_patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='family_doctor_id',
    )

    res_visit_ids = fields.Many2one(
        comodel_name='hr.hospital.visit',
    )
