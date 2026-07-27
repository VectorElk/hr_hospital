
from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalVisitReportWizard(models.TransientModel):
    _name = 'hr.hospital.visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
    )
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')
    only_completed = fields.Boolean(string='Only Completed Visits')
    condition_id = fields.Many2one(
        comodel_name='hr.hospital.condition',
        string='Condition',
    )

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end:
                start_date = record.date_start
                end_date = record.date_end
                if start_date > end_date:
                    raise ValidationError('Date Start must be earlier than or equal to Date End.')

    def default_get(self, fields_list):
        result = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids and self.env.context.get('active_id'):
            active_ids = [self.env.context['active_id']]

        if not isinstance(active_model, str) or not active_ids:
            return result

        active_records = self.env[active_model].browse(active_ids)

        if active_model == 'hr.hospital.doctor' and 'doctor_ids' in fields_list:
            result['doctor_ids'] = [Command.set(active_records.ids)]
        if active_model == 'hr.hospital.patient' and 'patient_ids' in fields_list:
            result['patient_ids'] = [Command.set(active_records.ids)]

        return result

    def action_open_report(self):
        self.ensure_one()

        domain = []
        if self.doctor_ids:
            domain.append(('res_doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('res_patient_id', 'in', self.patient_ids.ids))
        if self.date_start:
            domain.append(('date', '>=', self.date_start))
        if self.date_end:
            domain.append(('date', '<=', self.date_end))
        if self.only_completed:
            domain.append(('status', '=', '1'))
        if self.condition_id:
            domain.append(('condition_id', '=', self.condition_id.id))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit Report',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
            'context': {
                'search_default_completed': 1 if self.only_completed else 0,
            },
        }
