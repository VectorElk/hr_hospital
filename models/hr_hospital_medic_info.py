from odoo import api, fields, models


class HrHospitalMedicInfo(models.AbstractModel):
    _name = 'hr.hospital.medic.info'
    _description = 'Patient Medical Information'

    blood_type = fields.Selection([
        ('o_pos', 'O(I) Rh+'),
        ('o_neg', 'O(I) Rh-'),
        ('a_pos', 'A(II) Rh+'),
        ('a_neg', 'A(II) Rh-'),
        ('b_pos', 'B(III) Rh+'),
        ('b_neg', 'B(III) Rh-'),
        ('ab_pos', 'AB(IV) Rh+'),
        ('ab_neg', 'AB(IV) Rh-'),
    ])
    gender = fields.Selection([
        ("0", "Male"),
        ("1", "Female"),
    ])
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')

    @api.depends("birth_date")
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.context_today(record)
                record.age = (
                    today.year
                    - record.birth_date.year
                    - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
                )
            else:
                record.age = 0
