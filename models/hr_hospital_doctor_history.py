from odoo import api, fields, models


class HrHospitalDoctorHistory(models.Model):
    _name = 'hr.hospital.doctor.history'
    _description = 'History of personal doctors'

    res_patient_id = fields.Many2one('hr.hospital.patient', required=True)
    res_doctor_id = fields.Many2one('hr.hospital.doctor', required=True)
    start_date = fields.Date(required=True, default=fields.Date.context_today)
    end_date = fields.Date()
    active = fields.Boolean(default=True)

    display_name = fields.Char(compute='_compute_display_name', store=False)

    @api.depends('res_patient_id', 'res_patient_id.name', 'res_doctor_id', 'res_doctor_id.name',
                 'res_doctor_id.res_doctor_category_id.name', 'start_date')
    def _compute_display_name(self):
        for record in self:
            patient = record.res_patient_id.name or ''
            doctor = record.res_doctor_id.name or ''
            category = record.res_doctor_id.res_doctor_category_id.name or ''
            record.display_name = f"{patient} - {doctor} ({category}) {record.start_date}"

    @api.onchange('start_date', 'end_date')
    def _onchange_dates(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            self.end_date = False
            return {
                'warning': {
                    'title': 'Warning',
                    'message': 'Doctor change date cannot be earlier than assignment date.',
                }
            }
