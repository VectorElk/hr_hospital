import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class HRHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(required=True)
    emergency_contact = fields.Char()
    insurance_contact = fields.Char()
    age = fields.Integer()
    family_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        domain=[('is_family_doctor', '=', True)],
    )

    res_visit_ids = fields.Many2many(
        comodel_name='hr.hospital.visit',
    )
