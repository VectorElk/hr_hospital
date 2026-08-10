from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalVisitReportWizard(models.TransientModel):
    _name = 'hr.hospital.visit.report.wizard'
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    condition_ids = fields.Many2many(
        comodel_name='hr.hospital.condition',
        string='Conditions',
    )
    date_start = fields.Date(string='Date From')
    date_end = fields.Date(string='Date To')

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end:
                date_start = record.date_start
                date_end = record.date_end
                if date_start > date_end:
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
            result['doctor_ids'] = [(6, 0, active_records.ids)]
        return result

    def action_open_report(self):
        self.ensure_one()

        domain = []
        if self.doctor_ids:
            domain.append(('res_doctor_id', 'in', self.doctor_ids.ids))
        if self.date_start:
            domain.append(('date', '>=', self.date_start))
        if self.date_end:
            domain.append(('date', '<=', self.date_end))
        if self.condition_ids:
            domain.append(('condition_id', 'in', self.condition_ids.ids))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visit Report',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'target': 'current',
            'domain': domain,
            'context': {
                **self.env.context,
                'group_by': 'condition_id',
            },
        }
