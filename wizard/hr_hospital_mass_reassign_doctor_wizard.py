from odoo import _, fields, models
from odoo.exceptions import ValidationError


class HrHospitalMassReassignDoctorWizard(models.TransientModel):
    """Wizard to reassign multiple patients to a new doctor in batch.

    Updates personal_doctor_id for selected patients and creates audit trail
    in doctor history records with effective date.
    """
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = _('Mass Reassign Doctor to Patients')
    _transient_max_hours = 0.5
    _transient_max_count = 1000

    new_doctor_id = fields.Many2one(
        'hr.hospital.doctor',
        string=_('New Doctor'),
        required=True,
        help=_('Select the doctor to assign to selected patients')
    )
    date_changed = fields.Date(
        string=_('Date Changed'),
        default=fields.Date.context_today,
        required=True,
        help=_('Effective date for the doctor reassignment')
    )

    def action_mass_reassign(self):
        """Reassign selected patients to new doctor with audit trail.

        For each patient:
        1. Closes active doctor history record with end_date
        2. Updates personal_doctor_id to new doctor
        3. Creates new doctor history record with start_date

        Returns:
            dict: Success notification with count of reassigned patients.

        Raises:
            ValidationError: If no patients are selected.
        """
        doctor_label = self.new_doctor_id.display_name
        patient_ids = self.env.context.get('active_ids') or []

        if not patient_ids:
            raise ValidationError(_('No patients selected for reassignment.'))

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
                'title': _('Success'),
                'message': _('Successfully reassigned %s patient(s) to Dr. %s') % (len(patients), doctor_label),
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
