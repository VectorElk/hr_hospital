from odoo import fields, models
from odoo.exceptions import ValidationError


class HrHospitalMassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor to Patients'
    _transient_max_hours = 0.5
    _transient_max_count = 1000

    new_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string='New Doctor',
        required=True,
        help='Select the doctor to assign to selected patients'
    )
    date_changed = fields.Date(
        string='Date Changed',
        default=fields.Date.context_today,
        required=True,
        help='Effective date for the doctor reassignment'
    )

    def action_mass_reassign(self):
        patient_ids = self.env.context.get('active_ids', [])
        doctor_label = self.new_doctor_id.display_name

        if not patient_ids:
            raise ValidationError('No patients selected for reassignment.')

        patients = self.env['hr.hospital.patient'].browse(patient_ids)
        doctor_history_model = self.env['hr.hospital.doctor.history']

        for patient in patients:
            # Close any active doctor history record
            active_history = doctor_history_model.search([
                ('res_patient_id', '=', patient.id),
                ('end_date', '=', False),
            ])

            if active_history:
                active_history.write({
                    'end_date': self.date_changed,
                    'active': False
                })

            # Update patient's personal doctor
            patient.write({
                'personal_doctor_id': self.new_doctor_id.id
            })

            # Create new doctor history record
            doctor_history_model.create({
                'res_patient_id': patient.id,
                'res_doctor_id': self.new_doctor_id.id,
                'start_date': self.date_changed,
                'active': True
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': f'Successfully reassigned {len(patients)} patient(s) to Dr. {doctor_label}',
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
