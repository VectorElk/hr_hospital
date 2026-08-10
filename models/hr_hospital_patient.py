from odoo import _, fields, models


class HrHospitalPatient(models.Model):
    """Hospital Patient records with medical information and visit history.

    Tracks patient demographic and medical data, personal doctors, and family doctors.
    Linked to system users for access control.
    """
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.medic.info'
    _description = _('Hospital Patient')

    visit_count = fields.Integer(compute='_compute_visit_count')

    def _compute_visit_count(self):
        """Compute count of visits for this patient."""
        for record in self:
            record.visit_count = len(record.res_visit_ids)

    def action_view_patient_visits(self):
        """Open visit list filtered to this patient's visits.

        Returns:
            dict: Action window with filtered visit records.
        """
        action = self.env['ir.actions.act_window']._for_xml_id(
            'hr_hospital.action_hr_hospital_visit_window'
        )
        action['domain'] = [('res_patient_id', '=', self.id)]
        action['context'] = {
            'default_res_patient_id': self.id,
        }
        return action

    def action_quick_create_visit(self):
        """Quick action to create a new visit for this patient.

        Pre-fills patient and personal doctor in the new visit form.

        Returns:
            dict: Action window for creating a new visit.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_res_patient_id': self.id,
                'default_res_doctor_id': self.personal_doctor_id.id or False,
            },
        }

    name = fields.Char(required=True)
    phone = fields.Char()
    emergency_contact = fields.Char()
    insurance_contact = fields.Char()
    insurance_policy_number = fields.Char(size=20)
    res_system_user_id = fields.Many2one(
        comodel_name='res.users',
    )

    personal_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
    )

    personal_doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.history',
        inverse_name='res_patient_id',
    )

    family_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        domain=[('is_family_doctor', '=', True)],
    )

    res_visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='res_patient_id',
    )
