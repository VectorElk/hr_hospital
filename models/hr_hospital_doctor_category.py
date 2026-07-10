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

    def init(self):
        super().init()
        seed_values = {
            'hr_hospital.hr_hospital_doctor_category_intern': ('Doctor Intern', 10),
            'hr_hospital.hr_hospital_doctor_category_specialist': ('Doctor Specialist', 20),
            'hr_hospital.hr_hospital_doctor_category_highest': ('Doctor Highest Category', 30),
        }
        for xmlid, (name, sequence) in seed_values.items():
            category = self.env.ref(xmlid, raise_if_not_found=False)
            if category and (category.name != name or category.sequence != sequence):
                category.write({'name': name, 'sequence': sequence})
