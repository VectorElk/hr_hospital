import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)

class HrHospitalCondition(models.Model):
    _name = 'hr.hospital.condition'
    _description = 'Hospital Condition'

    name = fields.Char(required=True)
    description = fields.Char(required=True)
