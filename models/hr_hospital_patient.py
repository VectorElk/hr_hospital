from odoo import fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.medic.info'
    _description = 'Hospital Patient'

    visit_count = fields.Integer(compute='_compute_visit_count')

    def _compute_visit_count(self):
        for record in self:
            record.visit_count = len(record.res_visit_ids)

    def action_view_patient_visits(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'hr_hospital.action_hr_hospital_visit_window'
        )
        action['domain'] = [('res_patient_id', '=', self.id)]
        action['context'] = {
            'default_res_patient_id': self.id,
        }
        return action

    def action_quick_create_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'New Visit',
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
