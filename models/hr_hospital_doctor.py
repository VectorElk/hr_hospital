from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.medic.info'
    _description = 'Hospital Doctor'

    name = fields.Char(required=True)
    position = fields.Char(required=True)
    is_family_doctor = fields.Boolean(default=False)
    is_intern = fields.Boolean(compute='_compute_is_intern', store=True)
    intern_count = fields.Integer(compute='_compute_intern_display', store=False)
    intern_display_names = fields.Char(compute='_compute_intern_display', store=False)

    res_patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='family_doctor_id',
    )

    res_visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='res_doctor_id',
    )

    res_doctor_category_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.category',
    )

    res_system_user_id = fields.Many2one(
        comodel_name='res.users',
    )

    res_mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        domain=[('is_intern', '=', False)],
    )

    res_intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='res_mentor_id',
        string='Interns',
    )

    def action_quick_create_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Visit',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_doctor_id': self.id,
            },
        }

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.res_mentor_id = False

    @api.depends('res_doctor_category_id', 'res_doctor_category_id.name')
    def _compute_is_intern(self):
        intern_category = self.env.ref(
            'hr_hospital.hr_hospital_doctor_category_intern', raise_if_not_found=False
        )
        intern_category_id = intern_category.id if intern_category else False
        for record in self:
            record.is_intern = bool(record.res_doctor_category_id.id == intern_category_id)

    @api.depends('res_intern_ids', 'res_intern_ids.name')
    def _compute_intern_display(self):
        for record in self:
            intern_names = record.res_intern_ids.mapped('name')
            record.intern_count = len(intern_names)
            record.intern_display_names = ', '.join(intern_names)

    @api.constrains('is_intern', 'res_mentor_id')
    def _check_mentor_rules(self):
        for record in self:
            mentor = record.res_mentor_id
            if mentor and mentor == record:
                raise ValidationError('Doctor cannot be their own mentor.')
            if mentor and not record.is_intern:
                raise ValidationError('Only intern doctors can have a mentor.')
            if mentor and mentor.is_intern:
                raise ValidationError('Mentor cannot be an intern doctor.')
