from odoo import _, api, fields, models


class HrHospitalMedicInfo(models.AbstractModel):
    """Abstract base model for medical personnel (patients and doctors).

    Provides common medical fields: blood type, gender, birth date, and computed age.
    Inherited by Patient and Doctor models.
    """
    _name = 'hr.hospital.medic.info'
    _description = _('Patient Medical Information')

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
        ("male", _("Male")),
        ("female", _("Female")),
    ])
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age')

    @api.depends("birth_date")
    def _compute_age(self):
        """Calculate age in years from birth_date.

        Uses context date if available, otherwise uses current date.
        Sets age to 0 if birth_date is not set.
        """
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
