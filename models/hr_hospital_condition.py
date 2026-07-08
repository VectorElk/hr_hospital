from odoo import fields, models


class HrHospitalCondition(models.Model):
    _name = 'hr.hospital.condition'
    _description = 'Hospital Condition'

    name = fields.Char(required=True)
    description = fields.Char(required=True)

    res_visit_ids = fields.Many2many('hr.hospital.visit')
