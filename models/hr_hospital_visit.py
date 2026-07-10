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
        ('0', 'Planned'),
        ('1', 'Completed'),
        ('2', 'Canceled'),
    ])
    active = fields.Boolean(default=True)

    res_patient_id = fields.Many2one('hr.hospital.patient')
    res_doctor_id = fields.Many2one('hr.hospital.doctor')
    condition_id = fields.Many2one('hr.hospital.condition', string='Condition')

    def init(self):
        super().init()
        self.env.cr.execute("""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'hr_hospital_condition_hr_hospital_visit_rel'
            )
        """)
        if not self.env.cr.fetchone()[0]:
            return

        self.env.cr.execute("""
            UPDATE hr_hospital_visit AS visit
               SET condition_id = rel.hr_hospital_condition_id
              FROM (
                    SELECT hr_hospital_visit_id, MIN(hr_hospital_condition_id) AS hr_hospital_condition_id
                      FROM hr_hospital_condition_hr_hospital_visit_rel
                     GROUP BY hr_hospital_visit_id
                   ) AS rel
             WHERE visit.id = rel.hr_hospital_visit_id
               AND visit.condition_id IS NULL
        """)

    def write(self, vals):
        protected_fields = {'date', 'planned_date', 'visit_time', 'res_doctor_id'}
        if protected_fields.intersection(vals):
            completed_visits = self.filtered(lambda visit: visit.status == '1')
            if completed_visits:
                raise ValidationError('Cannot change schedule or doctor for completed visits.')

        if vals.get('active') is False:
            completed_visits = self.filtered(lambda visit: visit.status == '1')
            if completed_visits:
                raise ValidationError('Cannot archive completed visits.')

        return super().write(vals)

    def unlink(self):
        if self.filtered(lambda visit: visit.status == '1'):
            raise ValidationError('Cannot delete completed visits.')
        return super().unlink()
