from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    """Hospital Doctor records including staff, specialists, and interns.

    Manages doctor information, their mentor/intern relationships, patient assignments,
    and visit tracking. Supports role hierarchy from interns to fully qualified doctors.
    """
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.medic.info'
    _description = _('Hospital Doctor')

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
        string=_('Interns'),
    )

    def action_quick_create_visit(self):
        """Quick action to create a new visit for this doctor.

        Returns:
            dict: Action window for creating a new visit pre-filled with this doctor.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_doctor_id': self.id,
            },
        }

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        """Clear mentor when doctor is no longer an intern."""
        if not self.is_intern:
            self.res_mentor_id = False

    @api.depends('res_doctor_category_id', 'res_doctor_category_id.name')
    def _compute_is_intern(self):
        """Compute is_intern flag based on doctor category.

        A doctor is considered an intern if their category matches the intern category.
        """
        intern_category = self.env.ref(
            'hr_hospital.hr_hospital_doctor_category_intern', raise_if_not_found=False
        )
        intern_category_id = intern_category.id if intern_category else False
        for record in self:
            record.is_intern = bool(record.res_doctor_category_id.id == intern_category_id)

    @api.depends('res_intern_ids', 'res_intern_ids.name')
    def _compute_intern_display(self):
        """Compute display fields for managed interns.

        Sets intern_count and intern_display_names for doctors with interns.
        """
        for record in self:
            intern_names = record.res_intern_ids.mapped('name')
            record.intern_count = len(intern_names)
            record.intern_display_names = ', '.join(intern_names)

    @api.constrains('is_intern', 'res_mentor_id')
    def _check_mentor_rules(self):
        """Enforce mentor-intern relationship rules.

        Validates that:
        - Doctor cannot be their own mentor
        - Only interns can have mentors
        - Mentors must not be interns themselves

        Raises:
            ValidationError: If any mentor rule is violated.
        """
        for record in self:
            mentor = record.res_mentor_id
            if mentor and mentor == record:
                raise ValidationError(_('Doctor cannot be their own mentor.'))
            if mentor and not record.is_intern:
                raise ValidationError(_('Only intern doctors can have a mentor.'))
            if mentor and mentor.is_intern:
                raise ValidationError(_('Mentor cannot be an intern doctor.'))
