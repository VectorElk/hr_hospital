from odoo import _, fields, models
from odoo.exceptions import ValidationError


class HrHospitalVisit(models.Model):
    """Hospital Visit record tracking patient appointments with doctors.

    Handles visit scheduling, status tracking, and enforces business rules
    around completed visit modifications.
    """
    _name = 'hr.hospital.visit'
    _description = _('Hospital Visit')

    def _can_bypass_visit_restrictions(self):
        """Check if user has admin/system privileges to bypass visit restrictions.

        Returns:
            bool: True if user is admin or system user, False otherwise.
        """
        return self.env.user.has_group('hr_hospital.group_hr_hospital_administrator') or self.env.user.has_group('base.group_system')

    date = fields.Date(required=True)
    planned_date = fields.Datetime(required=True)
    visit_time = fields.Datetime(default=fields.Datetime.now)
    summary = fields.Html(required=True)
    status = fields.Selection([
        ('planned', _('Planned')),
        ('completed', _('Completed')),
        ('canceled', _('Canceled')),
    ])
    active = fields.Boolean(default=True)

    res_patient_id = fields.Many2one('hr.hospital.patient')
    res_doctor_id = fields.Many2one('hr.hospital.doctor')
    condition_id = fields.Many2one(
        'hr.hospital.condition',
        string=_('Condition (Legacy)'),
    )
    res_condition_id = fields.Many2one(
        'hr.hospital.condition',
        related='condition_id',
        string=_('Condition'),
        store=True,
        readonly=False,
    )
    same_condition_visit_count = fields.Integer(compute='_compute_same_condition_visit_count')

    def _compute_same_condition_visit_count(self):
        """Compute count of visits for each condition across all visits.

        Groups visits by condition and stores count in same_condition_visit_count field.
        """
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
        """Open all visits for the same condition as current visit.

        Returns:
            dict: Action window with filtered visits for the same condition.
        """
        action = self.env['ir.actions.act_window']._for_xml_id('hr_hospital.action_hr_hospital_visit_window')
        action['domain'] = [('res_condition_id', '=', self.res_condition_id.id)] if self.res_condition_id else [('id', '=', False)]
        action['context'] = {
            **self.env.context,
            'default_res_condition_id': self.res_condition_id.id,
        }
        return action

    def write(self, vals):
        """Prevent modification of completed visits.

        Completed visits cannot have their schedule or doctor changed,
        and cannot be archived.

        Args:
            vals (dict): Field values to write.

        Raises:
            ValidationError: If attempting to modify protected fields of completed visits.

        Returns:
            bool: Result of parent write operation.
        """
        protected_fields = {'date', 'planned_date', 'visit_time', 'res_doctor_id'}
        if protected_fields.intersection(vals):
            completed_visits = self.filtered(lambda visit: visit.status == 'completed')
            if completed_visits:
                raise ValidationError(_('Cannot change schedule or doctor for completed visits.'))

        if vals.get('active') is False:
            completed_visits = self.filtered(lambda visit: visit.status == 'completed')
            if completed_visits:
                raise ValidationError(_('Cannot archive completed visits.'))

        return super().write(vals)

    def unlink(self):
        """Delete visits with admin bypass for completed visits.

        Completed visits cannot be deleted except by admin/system users.

        Raises:
            ValidationError: If attempting to delete completed visits without proper permissions.

        Returns:
            bool: Result of parent unlink operation.
        """
        if self._can_bypass_visit_restrictions():
            return super().unlink()
        if self.filtered(lambda visit: visit.status == 'completed'):
            raise ValidationError(_('Cannot delete completed visits.'))
        return super().unlink()
