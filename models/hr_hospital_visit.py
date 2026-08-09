from odoo import fields, models
from odoo.exceptions import ValidationError


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Visit'

    date = fields.Date(required=True)
    planned_date = fields.Datetime(required=True)
    visit_time = fields.Datetime(default=fields.Datetime.now)
    summary = fields.Html(required=True)
    status = fields.Selection([
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ])
    active = fields.Boolean(default=True)

    res_patient_id = fields.Many2one('hr.hospital.patient')
    res_doctor_id = fields.Many2one('hr.hospital.doctor')
    condition_id = fields.Many2one(
        'hr.hospital.condition',
        string='Condition (Legacy)',
    )
    res_condition_id = fields.Many2one(
        'hr.hospital.condition',
        related='condition_id',
        string='Condition',
        store=True,
        readonly=False,
    )
    same_condition_visit_count = fields.Integer(compute='_compute_same_condition_visit_count')

    def _compute_same_condition_visit_count(self):
        counts = {}
        condition_ids = self.mapped('res_condition_id').ids
        if condition_ids:
            grouped_data = self.read_group(
                [('res_condition_id', 'in', condition_ids)],
                ['res_condition_id'],
                ['res_condition_id'],
            )
            for data in grouped_data:
                condition = data.get('res_condition_id')
                if condition:
                    counts[condition[0]] = data['res_condition_id_count']

        for record in self:
            record.same_condition_visit_count = counts.get(record.res_condition_id.id, 0)

    def action_view_same_condition_visits(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('hr_hospital.action_hr_hospital_visit_window')
        action['domain'] = [('res_condition_id', '=', self.res_condition_id.id)] if self.res_condition_id else [('id', '=', False)]
        action['context'] = {
            **self.env.context,
            'default_res_condition_id': self.res_condition_id.id,
        }
        return action

    def write(self, vals):
        protected_fields = {'date', 'planned_date', 'visit_time', 'res_doctor_id'}
        if protected_fields.intersection(vals):
            completed_visits = self.filtered(lambda visit: visit.status == 'completed')
            if completed_visits:
                raise ValidationError('Cannot change schedule or doctor for completed visits.')

        if vals.get('active') is False:
            completed_visits = self.filtered(lambda visit: visit.status == 'completed')
            if completed_visits:
                raise ValidationError('Cannot archive completed visits.')

        return super().write(vals)

    def unlink(self):
        if self.filtered(lambda visit: visit.status == 'completed'):
            raise ValidationError('Cannot delete completed visits.')
        return super().unlink()
