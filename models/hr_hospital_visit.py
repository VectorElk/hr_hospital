from odoo import fields, models


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Visit'

    date = fields.Date(required=True)

    res_patient_id = fields.Many2one('hr.hospital.patient')
    res_doctor_id = fields.Many2one('hr.hospital.doctor')
    res_condition_ids = fields.Many2many('hr.hospital.condition')
